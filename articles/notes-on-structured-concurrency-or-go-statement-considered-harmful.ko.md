title: Notes on structured concurrency, or: Go statement considered harmful
source: https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/

# 구조적 동시성에 대한 소고, 또는 Go 문의 해로움 


모든 동시성 API는 코드를 동시에 실행할 방법을 필요로 하죠. 서로 다른 API 들이 어떻게 생겼는지 한 번 볼까요.
    
    
    go myfunc();                                // Golang
    pthread_create(&thread_id, NULL, &myfunc);  /* C with POSIX threads */
    spawn(modulename, myfuncname, [])           % Erlang
    threading.Thread(target=myfunc).start()     # Python with threads
    asyncio.create_task(myfunc())               # Python with asyncio
    

다양한 표기법과 서로 다른 용어가 있겠지만, 문법적으로는 모두 같습니다. 모두 `myfunc`를 프로그램의 나머지 부분과 동시에 실행하려는 것이며, 즉시 돌아와 부모가 나머지 부분을 실행할 수 있도록 하는 것이죠.

다른 방법으로는 콜백을 사용하는 것도 있겠습니다.
    
    
    QObject::connect(&emitter, SIGNAL(event()),        // C++ with Qt
                     &receiver, SLOT(myfunc()))
    g_signal_connect(emitter, "event", myfunc, NULL)   /* C with GObject */
    document.getElementById("myid").onclick = myfunc;  // Javascript
    promise.then(myfunc, errorhandler)                 // Javascript with Promises
    deferred.addCallback(myfunc)                       # Python with Twisted
    future.add_done_callback(myfunc)                   # Python with asyncio
    

다시 한번, 표현만 다를 뿐 같은 일을 수행합니다. 지금부터 어떤 이벤트가 발생하면 `myfunc`를 실행하라는 것입니다. 한 번 설정되고 나면 즉시 되돌아와 부른 쪽에서 다른 일을 할 수 있게 되죠. (콜백이 [promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) [combinators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race), 또는 [Twisted-style protocols/transports](https://twistedmatrix.com/documents/current/core/howto/servers.html)와 같이 그럴싸해 보이는 형태로도 제공됩니다만, 결국 근간은 같습니다.)

그리고... 그렇죠. 실제로 사용되는 일반적인 동시성 API를 생각해보더라도 아마 둘 중 한쪽에 속할 겁니다 (가끔 asyncio와 같이 양쪽에 속하는 경우도 있죠).

하지만 제가 만든 새 라이브러리인 [Trio](https://trio.readthedocs.io)는 좀 다릅니다. 어느 쪽에도 해당하지 않죠. 대신, `myfunc`와 `anotherfunc`를 동시에 실행하고 싶다면, 아래와 같이 하면 됩니다.
    
    
    async with trio.open_nursery() as nursery:
        nursery.start_soon(myfunc)
        nursery.start_soon(anotherfunc)
    

"nursery" 구조를 처음 본 사람이라면 이게 뭔가 싶을 겁니다. 웬 들여쓰기가 있나? `nursery` 객체는 또 뭐고, 태스크를 실행하기 위해 왜 이런 걸 하나? 싶으실 겁니다. 그리고 나서는 다른 프레임워크에서 익숙하게 썼던 패턴을 사용하지 못해 짜증이 나겠죠. 기본 요소라기엔 기이하고 특이하며 너무 고급(high-level)처럼 느껴질 겁니다. 뭐 예상되는 반응입니다! 하지만 좀 참아보세요.

**이 포스트를 통해, 저는 nursery가 기이하지도 이상하지도 않으며, 반복문이나 함수 호출과 같은 근본적인 새로운 흐름 제어 방식임을 알리고자 합니다. 그리고, 위에서 봤던 기존의 방법 – 쓰레드 복제나 콜백 등록 – 들은 nursery로 완전히 대체되어야 한다고 봅니다.** 

이상하게 들리나요? 비슷한 일이 예전에도 있었습니다: 바로 `goto`가 흐름 제어의 시작과 끝이던 시절이 있었지만, 이젠 [다 흘러간 얘기](https://xkcd.com/292/)가 된 것처럼요. 몇몇 언어들이 아직 `goto`라 불리는 것을 가지고 있지만 예전에 `goto`라 불리던 것과 비교하면 다르고 기능이 제한되어 있습니다. 게다가 대부분의 언어에는 아예 없고요. 무슨 일이 있었냐고요? 옛날 옛적 일이라 아는 사람이 별로 없는 이야기지만 놀랄 정도로 유사한 이야기입니다. 그럼 이제 `goto`가 어떤 것이었는지 알아보는 걸로 시작해서 그 이야기가 왜 동시성 API에 대한 얘기로 이어지는지 알아봅시다.

## 도대체 `goto` 문이 뭐길래?

자, 역사를 살펴봅시다. 초기의 컴퓨터는 [어셈블리 언어](https://en.wikipedia.org/wiki/Assembly_language)나, 그보다 더 기초적인 방법들로 동작했습니다. 아주 거지 같았죠. 1950년대가 돼서야 IBM의 [존 배커스](https://en.wikipedia.org/wiki/John_Backus) 나 Remington Rand의 [그레이스 호퍼](https://en.wikipedia.org/wiki/Grace_Hopper) 같은 사람들이 [FORTRAN](https://en.wikipedia.org/wiki/Fortran)과 [FLOW-MATIC](https://en.wikipedia.org/wiki/FLOW-MATIC) (그 후속작인 [COBOL](https://en.wikipedia.org/wiki/COBOL)이 유명하죠) 같은 언어를 개발하기 시작했습니다.

이 시기의 FLOW-MATIC은 상당히 비범했습니다. 컴퓨터보다는 사람을 중시한 첫 번째 프로그래밍 언어로 파이썬의 할머니의 할아버지의 할머니 정도로 여겨도 됩니다. FLOW-MATIC 코드 맛 좀 볼까요.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-1.svg" style="width: 440px;" type="image/svg+xml"> </object>

현대적인 언어와는 다르게 `if`도 없고 반복문이나 함수 호출도 없군요. 알고 보면 블록 구분자와 들여쓰기조차 없습니다. 연속된 구문의 목록일 뿐입니다. 이 프로그램이 단지 짧거나 그럴싸한 제어 문법이 없어서가 아니라, 이 시절엔 아예 블록이라는 게 발명되지도 않았기 때문이죠!

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/sequential-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Sequential flow represented as a vertical arrow pointing down, and goto flow represented as an arrow that starts pointing down and then leaps off to the side.</object>

대신 FLOW-MATIC에는 두 가지 제어 방식이 있습니다. 보통은 예상한 대로 위에서 아래로 한 구문씩 순차적으로 실행됩니다. 하지만 `JUMP TO`같은 특별한 구문을 만나면 다른 곳으로 옮겨탑니다. 예를 들어, 구문(13)은 구문(2)로 점프합니다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-2.svg" style="width: 440px;" type="image/svg+xml"> </object>

제가 만든 동시성 기초 요소(역주: nursery)와 마찬가지로, 이 "단방향 점프"를 무엇으로 불러야 하는지 논란이 있었습니다. 여기서는 `JUMP TO`라고 했지만, 그 이름은 `goto`로 굳어지게 됩니다. ("go to" 같은 거죠) 여기서는 이렇게 부르겠습니다.

자, 이제 이 작은 프로그램의 완전한 `goto` 점프 구성을 봅시다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-4.svg" style="width: 440px;" type="image/svg+xml"> </object>

여러분만 이게 혼돈의 카오스로 보이는 건 아닙니다. 이런 식의 점프 기반 프로그래밍은 FLOW-MATIC이 어셈블리 언어로부터 직접적인 영향을 받은 것입니다. 강력하며, 컴퓨터 하드웨어가 동작하는 방식에 딱 맞지만, 직접적으로 사용하기에는 혼란스럽죠. 이 화살표 더미로부터 "스파게티 코드"라는 명칭도 나왔습니다. 더 나은 게 필요합니다.

흠... 이 모든 문제를 일으키는 `goto`란 무엇일까요? 왜 어떤 제어문은 괜찮고 어떤 건 안될까요? 어떻게 좋은 걸 고르죠? 당시에는 이게 명확하지 않기도 해서, 이해하지 못한다면 문제 해결이 정말 어려울 겁니다.

## `go` 문은?

하지만 잠깐, 모두가 `goto`가 나쁘다고 외치는 역사의 한순간에 멈춰볼까요? 이 얘기가 동시성과 관련이 있냐고요? 뭐, Golang의 유명한 `go` 문을 생각해봅시다. 새로운 "goroutine"(경량 쓰레드)을 만들어 보죠.
    
    
    // Golang
    go myfunc();
    

이 흐름을 다이어그램으로 그려볼까요? 음, 위에서 봤던 것과 좀 다릅니다. 흐름이 갈라지니까요. 그림으로 그려보면요,

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/go-schematic-unlabeled.svg" style="width: 395px;" type="image/svg+xml"> "Go" flow represented as two arrows: a green arrow pointing down, and a lavender arrow that starts pointing down and then leaps off to the side.</object>

일부러 _양쪽_ 선의 색상을 다르게 했습니다. 순차적으로 실행될 부모 goroutine(초록선)은 위에서 시작해서 즉시 아래로 진행합니다. 그동안 자식(라벤더색)은 위에서 시작해서 `myfunc` 본체로 점프합니다. 일반적인 함수 호출과 다르게, 이 점프는 단방향입니다. `myfunc`의 실행은 완전히 새로운 스택에서 이뤄지고, 런타임은 이 실행이 어디에서 시작되었는지도 모릅니다.

이건 Golang에만 해당하는 것은 아닙니다. 이 흐름은 글의 시작에 열거했던 _모든_ 기초 요소에 적용됩니다.

  * 쓰레딩 라이브러리는 일반적으로 나중에 쓰레드를 `join` 할 수 있는 객체를 제공합니다. 하지만 언어 차원에서는 알 수 없는 독립적인 작업입니다. 실제 쓰레드 복제 요소는 위와 같은 제어 흐름을 가집니다.
  * 콜백을 등록하는 것도 문법적으로는 다음과 같은 백그라운드 쓰레드를 시작하는 것과 같습니다. (a) 어떤 일이 발생할 때까지 멈춰있다가, (2) 콜백을 호출합니다. (구현은 완전히 다르게 되겠지만요.) 상위 수준의 흐름 제어로 보자면, 콜백 등록도 `go` 문과 동일합니다.
  * Future와 promise도 마찬가지입니다. promise를 돌려주는 함수를 호출하는 것은 백그라운드로 일어날 일을 예약한다는 것과 같습니다. 그리고 나중에 join할 객체를 – 원한다면 – 돌려줍니다. 흐름 제어 측면에서 보면, 쓰레드를 생성하는 방식과 같죠. 그리고 promise에 콜백을 등록하는 것이니 두 번 말할 것도 없습니다.

이 같은 패턴이 다양한 형태로 나타납니다. 이 다양한 형태의 핵심은 제어 흐름이 갈라지며, 한쪽은 단방향으로 점프하고 다른 한쪽은 호출했던 쪽으로 돌아간다는 것입니다. 뭘 봐야할 지 알게 되면, 같은 것을 여러 곳에서 찾아볼 수 있을겁니다 – 정말 즐거운 일이죠! [^1]

그런데, 이러한 흐름 제어를 부르는 공통된 이름이 없습니다. "`goto` 문"이 다른 `goto` 같은 구문을 통칭하는 이름이 된 것과 같이, 저도 이런 형태를 모두 "`go` 문"이라고 부르려고 합니다. 하필 왜 "go" 라고 묻는다면... Golang에 이러한 형태에 대한 명백한 예제가 있달까요. 어쨌든 이제 다들 제가 이걸 가지고 뭘 하려는지 알 것 같은데요. 이 두 다이어그램을 보세요. 비슷하지 않나요?

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/go-schematic-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Repeat of earlier diagrams: goto flow represented as an arrow that starts pointing down and then leaps off to the side, and "go" flow represented as two arrows: a green arrow pointing down, and a lavender arrow that starts pointing down and then leaps off to the side.</object>

맞아요. **go 문은 goto 문과 형태가 같습니다.**

동시성 프로그래밍은 작성하고 동작을 추론하기가 어려운 것으로 악명이 높죠. 마치 `goto`-기반 프로그램이 그러했던 것처럼요. 같은 이유로 그런 것은 아닐까요? 현대 언어들에서는 `goto` 문제가 상당수 해결되었죠. 우리가 `goto`를 해결한 것과 마찬가지로 이를 통해 사용하기 쉬운 동시성 API를 만들어낼 수 있을까요? 한 번 알아봅시다.

## `goto`에 무슨 일이 있었던 거야?

당최 `goto`가 뭐길래 이렇게 많은 문제를 낳았을까요? 1960년대 후반에 [에츠허르 데이크스트라](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra)는 [Go to의 해로움](https://scholar.google.com/scholar?cluster=15335993203437612903&hl=en&as_sdt=0,5)과 [구조적 프로그래밍에 대한 소고](https://www.cs.utexas.edu/~EWD/ewd02xx/EWD249.PDF) (PDF)와 같이 이 문제를 명확하게 설명하는, 근래에 매우 유명해진 글을 남겼습니다.

### `goto`: 추상화의 파괴자

그 문서들에서 데이크스트라는 비순차적 소프트웨어를 작성하고 잘 동작하게 만드는 문제에 대해 우려했습니다. 제가 이러한 통찰에 대해 감히 여기서 평가할 정도가 아니죠. 예를 들자면, 이런 얘기를 들어보셨을 겁니다.

![Testing can be used to show the presence of bugs, but never to show their absence!](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/testing.png)

이건 _구조적 프로그래밍에 대한 소고_에서 발췌한 것입니다. 하지만 그는 주로 _추상화_ 에 대해 신경을 썼습니다. 그는 머릿속에 다 담을 수 없을 정도로 거대한 프로그램을 만들고 싶어 했습니다. 이를 위해 프로그램의 각 부분을 블랙박스처럼 다룰 필요가 있죠. 파이썬 프로그램을 예로 들어보겠습니다.
    
    
     print("Hello world!")
    

문자열 포매팅, 버퍼 관리, 크로스플랫폼 이슈 등... `print`가 어떻게 구현되어 있는지 알 필요는 없습니다. 그저 당신이 입력한 문자열이 표시될 것이라는 것만 알면 코드의 다른 부분을 작성하는 데만 전념할 수 있습니다.  데이크스트라는 이러한 추상화가 프로그래밍 언어 수준에서 제공되길 원했습니다.

이것을 위해, 블록 문법이 발명되었고, ALGOL과 같은 언어에는 5가지 정도의 서로 다른 흐름 제어 구문이 있게 되었습니다. 여전히 순차적으로 실행되고 `goto`도 있었지만요.

앞서 나왔던 순차 진행과 goto 진행을 봅시다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/sequential-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Same picture of sequential flow and goto flow as before.</object>

그리고 비교문, 반복문, 함수 호출 등이 생겨났죠.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/control-schematics.svg" style="width: 500px;" type="image/svg+xml"> Diagrams with arrows showing the flow control for if statements, loops, and function calls.</object>

이 고급 기능을 `goto`로 만들 수도 있고, 초창기 사람들은 실제로 편리한 줄여 쓰기 정도로 여겼습니다. 하지만 데이크스트라는 다이어그램을 보면, `goto`와 다른 것들 사이에는 차이가 있다고 지적했습니다. `goto` 말고 나머지는 위에서 시작해서 → [뭔가 하고] 나서 → 아래로 내려가는 식으로 흘러갑니다. 이렇게 생겨 내부에서 뭘 하는지 신경 쓸 필요가 없는 모습을 "블랙박스 룰"이라고 불러보죠. [뭔가 하고] 부분을 무시하고 나면 전체적으로 봤을 때 그저 차례대로 흘러가는 것으로 볼 수 있습니다. 그리고 이런식으로 구성된 그 어떤 코드들에 대해서도 똑같이 여길 수 있으니까 좋죠. 이 코드를 다시 볼까요.
    
    
     print("Hello world!")
    

`print`의 정의나 그것의 전이적 의존성을 찾아보지 않더래도 일이 어떻게 돌아가는지 알 수 있습니다. `print` 안에 반복문이 있을 수도 있고, 그 반복문 안에 비교문이 있고, 또 그 안에 다른 함수 호출이 있고... 뭐 이것저것 있을 수 있죠. 하지만 뭔 상관이에요. `print` 내부로 흘러갔다가 그 안에서 뭔가 하고, 결국엔 제가 읽고 있는 코드로 돌아올 게 뻔하니까요.

되게 뻔한 것처럼 보이겠지만, 만약 `goto`가 있는 언어를, 아니, 모든 것들이 `goto` 위에서 만들어진 언어를 생각해보세요. 그리고 이 `goto`는 아무 때나 아무 곳으로나 갈 수 있죠. 이런 상황에서는 제어 구조가 전혀 블랙박스화 되지 않아요! 함수가 있는데, 그 함수 안에 반복문이 있어요. 그 안에 비교문이 있는데, 그 비교문 안에 `goto`가 있고... 그리고 `goto`는 어디든 간에 원하는 대로 가버릴 수 있죠. 호출한 적도 없는 완전히 다른 함수로 갑자기 가버릴 수도 있어요. 이걸 어떻게 알죠!

이렇게 추상화가 무너집니다. 다시 말하자면 이건 모든 함수 호출이 잠재적으로 `goto`의 변형된 형태라고 볼 수 있다는 것이고, 이걸 알려면 모든 시스템의 코드를 머릿속에 넣고 있어야 한다는 뜻입니다. 프로그래밍 언어에 `goto`가 있는 한, 흐름 제어의 지역적 추론이 불가능하다는 것입니다. 이래서 `goto`가 스파게티 코드를 만들게 되죠.

데이크스트라가 이 문제를 이해한 덕분에, 해결할 수 있었습니다. 이 혁명적인 제안을 보시죠. 우리는 비교문/반복문/함수 호출을 `goto`의 줄임말이라고 생각하지 말고, 각각의 기능이 있는 근본적인 기본 요소로 삼아야 합니다. 그러려면 `goto`를 우리 언어에서 완전히 쫓아내야 합니다.

2018년인 지금은 이 얘기가 굉장히 명확해 보입니다. 하지만 프로그래머에게서 그들이 충분히 똑똑하지 않아 불안하다는 이유로 장난감을 뺏았을 때 어떻게 반응하는지 본 적이 있나요? 네네, 이 세상엔 절대 변하지 않는게 있죠. 1969년에 이 제안은 엄청난 논쟁거리였습니다. [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth)는 `goto`를 [옹호](https://scholar.google.com/scholar?cluster=17147143327681396418&hl=en&as_sdt=0,5)했습니다. `goto`로 전문적인 코드를 작성하는 사람들이 더 제약이 심한 구조에서 다시 프로그래밍을 배워야 한다는 얘기에 분개하는 것도 무리는 아니었습니다. 물론 이를 위해 완전히 새로운 언어 세트를 만들어야 하기도 했으니까요.

![On the left, a photo of a snarling wolf. On the right, a photo of a grumpy bulldog.](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/wolf-and-bulldog.jpg)

왼쪽: 전통적인 `goto`. 오른쪽: 가축화된 `goto`로 C, C#, Golang 등에서 찾아볼 수 있다. 함수 경계를 넘을 수 없다는 것은, 이 녀석이 신발에 오줌을 쌀지언정, 얼굴을 물어뜯지 못한다는 것을 뜻한다.

결국, 현대 언어들은 데이크스트라의 원래 형식보다는 덜 엄격한 형태를 취했습니다. `break`, `continue`, `return` 등을 이용해서 중첩된 구조에서 한 번에 나올 수는 있죠. 하지만 근본적으로 그 경계가 제한된 방식 아래에서만 가능하니, 모두 데이크스트라의 아이디어에 근거하고 있다고 볼 수 있습니다. 특히, 흐름 제어를 감싸 블랙박스화하는데 쓰이는 "함수"는 불가침 영역입니다. 한 함수에서 다른 함수로 `break` 할 수 없고, `return`으로 함수에서 현재 함수에서 나올 수는 있지만, 더 이상은 불가합니다. 한 함수 내에서 내부적으로 지지고 볶는 흐름 제어를 한다고 해도, 다른 함수는 신경 쓸 거리 조차 없습니다.

이는 `goto` 그 자체에도 마찬가지입니다. C, C#, Golang과 같이 `goto`를 아직 가지고 있는 몇몇 언어들을 찾아볼 수 있습니다. 하지만 상당히 제한된 형태로 추가되어 있죠. 최소한 한 함수에서 다른 함수로 점프할 수 없을 겁니다. 역사적인 어셈블리[^2] 언어의 `goto`는 이제 안녕입니다. 데이크스트라 당신이 이겼어요.

### 의외의 이득: `goto`를 없앴더니 생긴 새로운 기능

`goto`가 없어지고 나니, 흥미로운 일이 일어났습니다. 언어 설계자들이 구조화된 흐름 제어에 의존하는 새로운 기능을 추가할 수 있게 되었습니다.

예를 들면, 파이썬은 자원을 비우기 위한 `with`라는 멋진 문법을 가지고 있습니다. 이렇게 쓸 수 있죠.
    
    
    # Python
    with open("my-file") as file_handle:
        ...
    

이는 `...` 코드가 실행되는 동안 파일이 열려 있다가, 종료되는 대로 바로 닫히는 것을 보장합니다. 대부분의 현대 언어들은 RAII, `using`, try-with-resource, `defer` 와 같은 비슷한 기능을 가지고 있습니다. 그리고 다들 질서 정연하고 체계적으로 코드가 실행될 것을 가정합니다. 우리가 `with` 블록 내에서 갑자기 `goto`를 쓰면 ... 어떻게 될까요? 파일은 열려있을까요 닫혀있을까요? 정상적으로 종료하는 대신에 그냥 점프해서 나가버린다면요? 파일은 닫힐까요? 이 기능은 언어에 `goto`가 있는 한 일관되게 동작할 수 없습니다.

에러 핸들링도 비슷한 문제가 있습니다. 뭔가 잘못되면 코드는 뭘 해야 할까요? 보통은 스택을 호출자에게 돌려주고 알아서 하라고 하는 쪽입니다. 현대적인 언어들은 이 문제를 쉽게 다룰 수 있도록 예외나, 이와 비슷한 형태의 [자동 오류 전파](https://doc.rust-lang.org/std/result/index.html#the-question-mark-operator-) 같은 것들을 가지고 있습니다. 하지만 이것도 스택과 "호출자"라는 신뢰할 수 있는 개념이 있는 경우에만 가능합니다. FLOW-MATIC 프로그램에 있던 흐름 제어를 놓고 그 안에서 예외가 발생했을 때 어떤 일이 일어날지 상상해보세요. 어디로 가야만 할까요?

### `goto` 문: 절대 안 돼요

`goto`, 그러니까 함수 경계를 넘나드는 과거의 `goto` 라는 건,  단순히 나쁘거나 제대로 쓰기 어려운 기능 정도가 아닙니다. 만약 그랬다면 수없이 많은 나쁜 기능에도 불구하고 살아남았을 겁니다. 하지만 그 정도 수준이 아닙니다.

> 스스로 `goto`를 사용하지 않는다고 해도, 그게 언어에 존재하는 한 모든 것을 사용하기 어렵게 됩니다. 써드 파티 라이브러리를 쓰려고 해도 블랙박스처럼 다룰 수 없습니다. 어떤 함수가 정상적인 함수인지 아니면 변칙적인 흐름을 가진 함수인지 알아내기 위해 모든 부분을 샅샅이 읽어봐야 합니다. 이래서는 지역적 추론을 할 수가 없습니다. 게다가 자원 정리나 자동 오류 전파 등의 기능도 쓸 수 없습니다. `goto`를 완전히 버리고 "블랙박스" 룰을 따르는 구조적 흐름 제어를 가지는 편이 낫습니다.

## `go` 문의 해로움

이렇게 `goto`의 역사를 살펴보았습니다. 이제 이걸 `go` 문에 적용해볼까요? 음... 기본적으로 하나부터 열까지 같아요. 과정이 놀랄 정도로 같습니다.

**Go 문은 추상화를 깨버립니다.** `goto`가 가능한 언어에서 어떤 기능들이 `goto`의 다른 형태로 나타나는지 기억나시나요? 대부분의 동시성 프레임워크에서 `go` 문은 같은 문제를 일으킵니다. 함수를 호출할 때마다 백그라운드 작업이 생성되거나 생성되지 않을 수 있습니다. 함수는 돌아온 것 같지만 백그라운드에서 아직 실행 중일까요? 소스 코드를 다 읽기 전까지는 알 도리가 없죠. 작업은 언제 종료될까요? 답하기가 어렵군요. `go` 문이 있는 한, 함수는 흐름 제어와 관련해서 더 이상 블랙박스가 될 수 없습니다. 제가 썼던 [첫 번째 동시성 API에 대한 글](https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/)에서 "인과율 위반"이라 칭한 이것이, 다양한 실제적인 문제들의 근본적인 원인임을 찾아냈습니다. asyncio와 Twisted에서의 배압 문제, 제대로 종료되지 않는 문제 등이요.

**Go 문은 자동 자원 정리를 불가능하게 합니다.** `with`를 예로 들어 보겠습니다.
    
    
    # Python
    with open("my-file") as file_handle:
        ...
    

앞서, 우리는 `...` 코드가 실행되는 동안 파일이 열려 있을 것을 "보장"받고, 끝나면 닫힌다고 얘기했었죠. 하지만 `...` 코드에서 백그라운드 작업을 생성한다면 어떻게 될까요? 더 이상 보장할 수 없게 됩니다. `with` 블록 안에 있는 것처럼 보였던 동작이 실제로는 `with` 블록이 끝나도 계속 동작하고 있을 수 있고, 그러다가 파일이 닫히면 사용하고 있던 쪽에서는 오류가 발생할 수 있습니다. 다시 한 번 얘기하지만, 이런 식으로는 부분만 봐서 알 수 없게 됩니다. `...` 코드에서 호출되는 함수의 모든 소스 코드를 살펴봐야만 합니다.

이 코드를 제대로 돌아가게 하려면, 백그라운드로 동작하는 작업들을 어떻게든 추적하고 완료될 때까지 기다려서 파일을 닫아야 합니다. 뭐 가능한 일이긴 하죠. 작업이 끝났을 때 알려주는 라이브러리를 사용하는 한 괴롭긴 하지만 할 수는 있습니다. (예: 나중에 다시 만날(join) 수 있도록 하는 핸들을 제공하지 않는 경우) 하지만 아무리 최상의 상황을 가정해봐도 비구조적인 흐름 제어하에서는 언어 차원에서 도움을 줄 수가 없습니다. 다시 옛날처럼 수작업으로 자원 정리를 해야만 하겠죠.

**Go 문은 오류를 다루지 못하게 합니다.** 위에서 얘기했던 것과 같이, 현대의 언어들은 오류를 검출하고 제대로 전파하는 데 도움을 주는 예외와 같은 강력한 도구를 제공합니다. 하지만 이 도구들도 신뢰할 수 있는 "현재 코드의 호출자"라는 개념에 의존하고 있습니다. 작업을 생성하고 콜백을 등록하면 이 개념은 바로 무너집니다. 제가 아는 한, 많이 사용되는 대부분의 동시성 프레임워크들은 이를 그냥 포기했습니다. 백그라운드 작업에서 오류가 발생했는데, 그걸 수동으로 처리하지 않았다면 런타임은... 이걸 그냥 대충 치워버리고 사실은 중요하지 않았다는냥 행세를 하죠. 운이 좋다면 콘솔에 뭐라도 찍을 수 있었겠네요. (제가 이제까지 썼던 소프트웨어들 중에 "뭔가 인쇄하고 계속 수행해버린다" 전략이 그럭저럭 통했던건 쉰내 나는 포트란 라이브러리 정도였습니다. 이제와서 그러면 안 되죠.) 심지어 Rust마저도 – 전국 고등학생 투표 결과 쓰레드 정합성에 가장 집착한 언어로 꼽힌 – 면죄부를 받을 수는 없습니다. Rust는 [오류를 버리고 잘 되기를 기원](https://doc.rust-lang.org/std/thread/)하는 편이죠.

물론 이런 시스템에서도 쓰레드 결합을 조심스럽게 다루거나 [Twisted의 errbacks](https://twistedmatrix.com/documents/current/core/howto/defer.html#visual-explanation)나 [JavaScript의 Promise.catch](https://hackernoon.com/promises-and-error-handling-4a11af37cb0e)처럼 자체적인 오류 전파 구조를 작성해서 오류를 제대로 다룰 수는 있습니다. 하지만 이미 언어에 있는 기능을 임시변통으로 재구현한 것뿐이죠. "역추적"이나 "디버거" 등의 기능은 다 갖다 버리고서요. `Promise.catch` 한 번만 까먹었다간 갑자기 알아채지도 못했던 심각한 문제가 발생하고 말 겁니다. 이 모든 문제를 해결했다 치더라도, 똑같은 일을 하는 두 개의 너저분한 시스템과 함께해야 할 뿐입니다.

### `go` 문: 절대 안 돼요

`goto`가 최초의 고급 프로그래밍 언어에서 기초 요소로 존재했던 것과 같이, `go` 또한 최초의 실용적 동시성 프레임워크에서는 당연히 기초 요소 대접을 받았습니다. 기본 스케쥴러가 실제로 동작하는 방식과 일치하고, 그 어떤 동시성 흐름 패턴도 구현할 만큼 강력하죠. 하지만 `goto`가 그랬던 것처럼, 추상화를 깨트려, 이게 언어에 존재한다는 것만으로도 모든 일이 어려워집니다.

그럼에도 좋은 소식이 있다면, 이 문제는 이미 완전히 해결되었다는 것이죠. 데이크스트라가 보여줬잖아요? 뭘 해야 하나면,

  * `go`와 같은 기능을 가진 비슷한 것 중에서, "블랙박스 룰"을 따르는 것을 찾기.
  * 동시성 프레임워크에 새로운 구조를 기초 요소로 만들고, `go` 같은 건 포함하지 말기.

이게 바로 Trio가 하는 것입니다.

## Nursery: `go`를 대체하는 구조적 용법

핵심 아이디어를 말씀드리겠습니다. 흐름이 여러 갈래로 갈라질 때마다, 다시 합쳐지는 것을 명확하게 하고자 합니다. 세 가지 일을 한꺼번에 하는 경우를 예로 들자면, 흐름 제어는 아래와 같을 겁니다.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-schematic-unlabeled.svg" style="width: 250px;" type="image/svg+xml"> </object>

하나의 화살표가 위에서 그대로 아래로 가고 있는 것에 주목해 주세요. 바로 데이크스트라의 블랙박스 룰을 따른다는 것이죠. 이제, 이 모습을 어떻게 언어의 견고한 요소로 만들 수 있을까요? 이 제약에 걸맞은 몇 가지 구조가 있습니다만, (a) 제가 제안하려는 건 이제까지의 것들과 조금은 다르고요(특히 독립 실행형 요소로 만들고 싶다는 점에서), (b) 동시성과 관련된 이야기는 너무 방대하고 복잡해서 역사를 따지고 장단점을 구분하려면 삼천포로 빠지는 일이라, 나중에 따로 적도록 하겠습니다. 이 글에서는 제 솔루션을 설명하는 데 집중하겠습니다. 하지만 제가 동시성과 관련된 뭔가를 발명했다는 얘기를 하려는 게 아니고, 여러 곳에서 영감을 끌어다 썼으며, 그저 거인의 어깨 위에서 서 있다는 것만 알아주세요. [^3]

어쨌거나, 이렇게 해보려고 합니다. 먼저, 부모 작업에서 nursery라 불리는 자식을 위한 장소를 마련하지 않는 한, 그 어떤 자식 작업도 시작하지 못한다고 합시다. _nursery 블록_을 열어서 시작하죠. 트리오에서는 이걸 `async with` 문법으로 사용합니다.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-1-pathified.svg" style="width: 350px;" type="image/svg+xml"> </object>

nursery 블록을 엶과 동시에 이 nursery를 나타내는 객체가 생성되고, `as nursery` 문법을 통해 이를 `nursery` 라는 변수에 할당합니다. 그 다음 nursery 객체의 `start_soon` 기능을 통해 동시 작업을 시작할 수 있습니다. 이 경우에 한 작업은 `myfunc` 함수를 호출하고, 다른 하나는 `anotherfunc`를 호출하게 됩니다. 개념적으로 이 작업들은 nursery 블록 _내부_에서 실행됩니다. nursery 블록의 코드들은 블록이 생성됨과 동시에 시작되는 초기 작업들이라고로 생각하면 편합니다.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-2-pathified.svg" style="width: 500px;" type="image/svg+xml"></object>

결정적으로, nursery 블록은 그 안의 모든 작업이 종료될 때까지 끝나지 않습니다. 자식 작업이 모두 끝나기 전에 부모 작업이 끝에 다다르면, 멈춰서 끝나길 기다립니다. Nursery가 자동으로 확장되어 자식들을 기다리는 것이죠.

이 흐름을 보시면 이 섹션의 첫 부분에 보여드린 것과 같은 패턴임을 확인할 수 있습니다.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-3-pathified.svg" style="width: 600px;" type="image/svg+xml"> </object>

이 그림은 여러 중요한 내용을 담고 있지만, 모두 명확하지는 않습니다. 하나씩 알아보죠.

### Nursery는 함수 추상화를 보존합니다.

`go` 문의 근본적인 문제는 함수를 호출할 때, 함수가 종료된 뒤에도 백그라운드 작업을 생성하는지 여부를 알 수 없다는 데 있습니다. Nursery와 함께라면 이런 걱정을 할 필요가 없죠. 어떤 함수라도 nursery를 열고 여러 동시 작업을 실행할 수 있지만, 모두 끝날 때까지 함수는 반환되지 않을 겁니다. 그러니까 함수에서 돌아왔다면, 실제로 끝난 겁니다.

### Nursery는 동적 작업 복제를 지원합니다.

위의 흐름 제어 다이어그램을 충족시키는 더 단순한 형태가 있습니다. 썽크 목록을 받아 모두 동시에 실행합니다.
    
    
    run_concurrently([myfunc, anotherfunc])
    

이런 부류의 문제점은 실행하기 전에 모든 작업의 목록을 알아야 한다는 데 있습니다. 늘 그럴 순 없죠. 예를 들어, 일반적인 서버 프로그램들이 가지고 있는 `accept` 루프는 들어오는 연결을 받아 개별적인 처리를 위해 새로운 작업을 시작합니다. Trio로 구현된 최소한의 `accept` 루프를 보시죠.
    
    
    async with trio.open_nursery() as nursery:
        while True:
            incoming_connection = await server_socket.accept()
            nursery.start_soon(connection_handler, incoming_connection)
    

Nursery에서는 굉장히 쉬운 일이지만, `run_concurrently` 같은 것으로 구현하려면 _훨씬_ 버거울 겁니다. 원한다면 nursery 상에서도 `run_concurrently` 를 구현할 수 있겠지만, 그 정도로 단순한 경우에는 Nursery 표기법이 훨씬 읽기 쉬우니 그럴 필요가 없습니다. 

### 탈출구가 있습니다.

Nursery 객체는 탈출구도 제공합니다. 백그라운드 작업이 그 자체보다 더 오래 걸리는 백그라운드 작업을 생성하는 경우에는 어떻게 할까요? 간단합니다. 함수에 Nursery 객체를 전달하면 됩니다. `async with open_nursery()` 블록 안에서만 `nursery.start_soon`을 호출하라는 법은 없습니다. Nursery 블록이 열려 있는 한[^4], nursery 객체에 참조를 얻을 수 있는 누구라도 nursery 내에 작업을 생성할 수 있습니다. 함수 인자로 전달하거나 대기열에 넣거나, 뭐든지요.

실제로는, 이는 "규칙을 어기는" 함수를 작성할 수 있음을 의미합니다. 몇 가지 제약이 있지만요.

  * Nursery 객체를 명시적으로 전달해야 하므로, 일반적인 흐름 제어를 위반하는 경우를 호출하는 시점에서 즉시 알아낼 수 있습니다. 여전히 지역 추론은 가능합니다.
  * 함수가 생성한 작업들은 전달된 nursery 객체와 생사를 같이하게 됩니다.
  * 호출하는 코드는 자체적으로 접근할 수 있는 nursery 객체 내에서만 전달될 수 있습니다.

그러므로 임의의 코드가 무한한 수명을 가진 백그라운드 작업을 생성할 수 있는 기존 모델과는 차별됩니다.

이를 통해 Nursery가 `go`문과 동등한 표현력을 가짐을 증명할 수도 있지만, 이미 글이 기어지고 있어 따로 적도록 하겠습니다.

### Nursery처럼 동작하는 새로운 타입을 정의할 수 있습니다.

기본 nursery 문법으로도 충분한 토대를 제공할 수 있지만, 때로는 특별한 것을 원하는 경우도 있습니다. Erlang과 그것의 supervisors가 부러워 nursery 유사 클래스에서 자식 작업을 재시작하는 식으로 예외를 다루고 싶은 경우에도 사용될 수 있습니다. 일반적인 nursery와 비슷합니다.
    
    
    async with my_supervisor_library.open_supervisor() as nursery_alike:
        nursery_alike.start_soon(...)
    

Nursery를 인자로 받는 함수가 있을 때, 생성된 작업을 위해 오류 처리를 위한 정책을 제어하는 대신 nursery를 인자로 전달할 수 있습니다. 멋지네요. Trio를 asyncio나 다른 라이브러리들과 구별되게 하는 미묘한 부분이 있습니다. 바로 `start_soon`이 coroutine 객체나 `Future`가 아닌 함수를 받는다는 점입니다. (함수는 여러 번 실행될 수 있지만, coroutine 객체나 `Future`는 그럴 수 없으니까요.) 이게 여러 가지 이유에서(특히 Trio는 `Future` 같은 게 필요 없으니까) 더 나은 문법이라고 생각하지만, 언급할 필요는 있겠죠

### 아니요, 사실, nursery는 _항상_ 내부 작업이 끝나기를 기다립니다.

잘못 사용하는 경우에 한해서지만, nursery 불변성을 깨트리는 미묘한 부분이 있을 수 있으므로, 어떻게 작업이 취소되며 작업 결합이 이뤄지는지 설명할 필요가 있겠습니다.

Trio에서 코드는 언제든지 취소 요청을 받을 수 있습니다. 취소가 요청되면, 코드는 그 후에 "체크포인트" 작업을 수행하고, `Cancelled` 예외를 발생시킵니다. 즉, 취소가 _요청된_ 시점과 실제로 취소가 _수행된_ 시점에 차이가 있다는 것입니다. 작업이 체크포인트를 실행하기까지 시간이 걸리고, 그 이후에 예외가 스택을 따라 돌아가 청소하는 작업을 수행하거나 합니다. 이러한 일이 생겨도, nursery는 청소 작업이 항상 완전히 수행될 때까지 기다립니다. 청소할 기회조차 주지 않고 작업을 종료해 버리거나 완전히 취소되지 않은 상태로 남겨지는 일은 _절대로_ 일어나지 않습니다.

### 자동으로 자원을 비웁니다.

Nursery는 블랙박스 룰을 따르기에, `with` 블록을 다시 사용할 수 있습니다. `with` 블록의 끝에 도달해 파일을 닫아버리는 바람에 백그라운드로 동작하던 작업이 갑자기 종료하는 일은 없습니다.

### 자동으로 오류를 전파합니다.

위에서 말했듯, 대부분의 동시성 시스템은 백그라운드 작업에서 다루지 못한 에러는 그냥 무시해버리는 편입니다. 말 그대로 그걸로 뭘 할 수 없기 때문입니다.

Trio에서는 모든 작업이 nursery 안에서 이뤄지는데, 모든 nursery는 부모 작업의 일부이므로, 부모 작업은 nursery 내의 작업이 끝나기를 기다려줘야 합니다. 그러니 처리되지 않은 오류를 _제대로_ 다룰 수 있습니다. 백그라운드 작업이 예외와 함께 종료되면, 부모 작업으로 예외를 돌려보낼 수 있습니다. 여기서 nursery를 "동시 호출"을 수행하는 기초 요소로 본다는 것이 핵심입니다. `myfunc`와 `anotherfunc`를 동시에 호출하는 예제에서 호출 스택이 트리로 구성됩니다. 그러므로 예외는 일반적인 호출 스택과 같이 트리 구조를 따라 전파될 수 있습니다.

부모 작업에서 예외를 다시 발생시키면, 부모 작업 내에서 전파가 시작된다는 점이 미묘합니다. 일반적으로 이는 부모 작업이 nursery 블록을 종료시킨다는 의미입니다. 하지만 앞서 부모 작업은 자식 작업이 실행되는 동안 nursery 블록을 벗어날 수 없다고 말했었죠. 어떻게 해야 할까요?

자식에서 처리되지 않은 예외가 발생하면 Trio가 nursery 내의 다른 작업을 모두 취소하고 완료될 때까지 기다린 뒤에 예외를 다시 발생시키는 식으로 이 문제를 처리합니다.

이는 프로그래밍 언어에서 nursery를 구현할 때, nursery 코드와 취소 시스템 사이에 일종의 통합이 필요할 수도 있다는 것을 의미합니다. 취소를 위해 객체를 수동으로 전달해야 하는 관례를 가진 C# 이나 Golang과 같은 언어나 일반적인 취소 구현이 없는 언어에서는 다소 까다로운 작업이 될 겁니다.

### 의외의 이득: `go`를 없앴더니 생긴 새로운 기능

`goto`를 없애므로 언어 설계자들이 프로그램 구조에 대해 보다 명확한 가정을 할 수 있게 되어 만들 수 있었던 `with` 블록과 예외 처리와 같이, `go`를 없앰으로 비슷한 효과가 있었습니다.

  * Trio의 취소 시스템은 작업이 일반적인 트리 구조로 이루어져 있다고 가정할 수 있어, 경쟁자들에 비해 더 쉽고 안정적으로 사용할 수 있습니다. [인간을 위한 시간제한과 취소](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/)를 통해 확인해보세요.
  * Trio는 파이썬 개발자가 기대하는 방식으로 control-C가 동작하는 유일한 파이썬 동시성 라이브러리입니다. ([자세히](https://vorpus.org/blog/control-c-handling-in-python-and-trio/)) 이는 nursery와 같이 예외 전파를 위한 신뢰할 수 있는 구조를 제공하지 않으면 불가능한 일입니다.



## Nursery를 써보자

이제까지 이론적인 것을 알아봤습니다. 실제로는 어떨까요?

음... 경험적인 질문이군요. 직접 해봐야 알 수 있습니다! 하지만 정말 진지하게 경험해보지 않으면 알 수 없는 부분이 많겠죠. 이 지점에서는 제 얘기가 꽤 그럴싸하게 들릴 거라 확신하긴 하지만, 초기의 구조적 프로그래밍 옹호론자들이 `break`와 `continue`를 허용하며 물러난 것과 같이 약간의 변경이 필요하다는 것은 인정해야 할지도 모릅니다.

만약 당신이 경험이 많은 동시성 프로그래머라면 Trio를 배우는데 좀 거친 시간을 보내야 합니다. 1970년대의 프로그래머가 `goto` 없이 코드를 배우느라 고생했던 것과 같이 [새로운 방식으로 일하는 법](https://stackoverflow.com/questions/48282841/in-trio-how-can-i-have-a-background-task-that-lives-as-long-as-my-object-does)을 배우기도 해야 합니다.

물론 그게 핵심이죠. 크누스는 이렇게([Knuth, 1974](https://scholar.google.com/scholar?cluster=17147143327681396418&hl=en&as_sdt=0,5), p. 275) 말했습니다.

> 아마도 `go to`문과 관련하여 저지를 수 있는 가장 큰 실수는 늘 하던 대로 프로그램을 작성한 다음에 **go to**만 싹 제거한 다음에 "구조적 프로그래밍"이라고 부르는 것일 겁니다. 대부분의 **go to**는 애초에 있어야 하지 않을 곳에 있는 겁니다. 우리가 정말로 원하는 것은 애초에 **go to**문을 _생각조차_ 하지 않고 프로그램을 구상하는 것이기 때문입니다. 그게 반드시 필요한 곳은 사실상 거의 없기 때문입니다. 우리가 언어를 통해 아이디어를 구현하는 것은 우리의 사고 과정에 강한 영향을 받습니다. 그런 연유로 데이크스트라는 복잡성에 대한 **go to**의 유혹을 피할 수 있는 언어의 새로운 기능들, 즉 명확한 사고를 장려하는 구조를 요구했던 것입니다. 

그리고 제가 이제까지 nursery를 사용한 경험이 바로 그것입니다. 이는 저를 명확한 사고로 이끌었습니다. 더 견고하고, 사용하기 쉬우며, 전체적으로 나은 디자인으로 이어집니다. 제약 사항들 덕에 불필요한 복잡도를 다루는 일에서 벗어나 문제를 더 쉽게 해결할 수 있게 됩니다. Trio를 사용하는 것은, 실질적인 의미에서 제가 더 나은 프로그래머가 되도록 이끌어 주었습니다.

TCP 연결 맺는 속도를 높이는 단순한 동시성 알고리즘인 Happy Eyeballs 알고리즘([RFC 8305](https://tools.ietf.org/html/rfc8305))을 생각해봅시다. 개념적으로, 이 알고리즘은 복잡하지 않습니다. 네트워크에 과부하가 걸리지 않도록 시차를 두고 서로 경쟁적으로 연결을 시도하게 하는 것입니다. 그러나 [Twisted의 최적 구현체](https://github.com/twisted/twisted/compare/trunk...glyph:statemachine-hostnameendpoint)는 거의 600줄에 달하는 파이썬 코드이며, [여전히 하나의 로직 버그](https://twistedmatrix.com/trac/ticket/9345)를 가지고 있는 것을 알 수 있습니다. Trio로 구현한 동일한 결과물의 길이는 1/15밖에 되지 않습니다. 더 중요한 것은, Trio를 사용하여 몇 달이 아니라 몇 분 만에 작성할 수 있었고, 단박에 정확한 로직을 구현했다는 것입니다. 제가 오랫동안 사용했던 그 어떤 프레임워크로도 이렇게 하진 못했습니다. [지난 달에 Pyninsula에서의 제 발표](https://www.youtube.com/watch?v=i-R704I8ySE)를 살펴봐 주세요. 뻔한 이야기인가요? 하지만 시간이 말해주겠죠. 저는 유망하다고 봅니다.

## 결론

인기 있는 동시성 요소들인 – `go`문, 쓰레드 복제 함수, 콜백, futures, promises, ... 이런 것들은 이론적으로도 실제적으로도 모두 `goto`의 변형일 뿐입니다. 게다가 현대화된 `goto`도 아니고 함수 경계를 넘나드는, 호랑이 담배 피우던 시절의 `goto` 수준입니다. 이런 요소들은 우리가 직접 사용하지 않더래도 매우 위험합니다. 우리가 흐름을 읽어내는 것도 방해하며, 추상화된 모듈식 구성으로 복잡한 시스템을 만들지도 못하게 하며, 자동화된 자원 정리와 오류 전파와 같은 언어 수준의 유용한 기능도 쓰기 힘들게 만들기 때문입니다. 그 결과, 현대의 고급 언어에는 `goto`는 갈 곳이 없어졌죠.

Nursery는 언어의 기능을 해치지 않으며 안전하고 편리한 대안을 제공할 뿐 아니라, 강력한 새로운 기능(Trio의 취소 범위와 control-C 처리로 입증된)을 제공합니다. 이는 가독성과 생선성, 정확한 구현의 극적인 향상을 이끌어 냅니다.

아쉽게도, 이러한 이점을 충분히 가져가려면, 기존 요소를 완전히 제거하고 아마도 바닥부터 완전히 새로운 동시성 프레임워크를 만들어야 할지도 모릅니다. `goto`가 없는 새로운 언어를 설계하는 것과 같이요. 하지만 FLOW-MATIC이 나왔을 당시에 인상적이었던 것만큼, 더 좋은 나은 무언가로 좋아지는 것은 반길만한 일입니다. 저는 nursery로 전환하는 것을 후회할 거라 생각하지 않습니다. Trio를 통해 이것이 실용적이며 범용적인 동시성 프레임워크 디자인임은 입증했다고 생각합니다.

## 붙임

초안을 검토해준 Graydon Hoare, Quentin Pradet, 그리고 Hynek Schlawack에게 감사드립니다. 남아있는 오류는 모두 제 탓입니다.

저작권: FLOW-MATIC 샘플 코드는 [컴퓨터 역사 박물관](http://www.computerhistory.org/collections/catalog/102646140)이 보관중인 [이 브로슈어](http://archive.computerhistory.org/resources/text/Remington_Rand/Univac.Flowmatic.1957.102646140.pdf) (PDF)에서 발췌.  [Wolves in Action](https://www.flickr.com/photos/iam_photo/478178221), by i:am. photography / Martin Pannier, [CC-BY-SA 2.0 라이센스](https://creativecommons.org/licenses/by-nc-sa/2.0/), cropped.  [French Bulldog Pet Dog](https://pixabay.com/en/french-bulldog-pet-dog-funny-2427629/) by Daniel Borker, released under the [CC0 public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

## 각주

[^1]: 최소한 특정 부류의 인간에게는.  
[^2]: WebAssembly는 `goto` 없이도 충분히 저수준 언어로 사용될 수 있음을 보여주었다: [reference](https://www.w3.org/TR/wasm-core-1/#control-instructions%E2%91%A0), [rationale](https://github.com/WebAssembly/design/blob/master/Rationale.md#control-flow)  
[^3]: 제가 관심을 기울이고 있는 논문이 어떤 것인지 모르고는 도저히 집중할 수 없는 분들을 위해 알려드리자면, 이 리뷰에 포함된 논문 목록은 다음과 같습니다: the "parallel composition" operator in Cooperating/Communicating Sequential Processes and Occam, the fork/join model, Erlang supervisors, Martin Sústrik's article on [Structured concurrency](http://250bpm.com/blog:71) and work on [libdill](https://github.com/sustrik/libdill), and [crossbeam::scope](https://docs.rs/crossbeam/0.3.2/crossbeam/struct.Scope.html) / [rayon::scope](https://docs.rs/rayon/1.0.1/rayon/fn.scope.html) in Rust. Edit: I've also been pointed to the highly relevant [golang.org/x/sync/errgroup](https://godoc.org/golang.org/x/sync/errgroup) and [github.com/oklog/run](https://godoc.org/github.com/oklog/run) in Golang. 제가 빼먹은 중요한게 있다면 [알려주세요](mailto:njs@pobox.com).  
[^4]: Nursery 블록이 종료된 _후에_ `start_soon`을 호출하면 `start_soon`은 오류를 발생시키고, 만약 오류가 발생하지 않는다면, nursery 블록은 남은 작업이 끝날 때까지 열린 상태로 유지될 것입니다. 직접 nursery 시스템을 구현하는 경우에 이 부분의 동기화를 신중하게 다뤄야 합니다.
