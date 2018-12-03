title: Notes on structured concurrency, or: Go statement considered harmful
source: https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/

# 구조적 동시성에 대한 소고, 또는 Go 구문의 해로움 


모든 동시성 API는 코드를 동시에 실행할 수 있는 방법을 필요로 하죠. 서로 다른 API 들이 어떻게 생겼는지 한 번 볼까요.
    
    
    go myfunc();                                // Golang
    pthread_create(&thread_id, NULL, &myfunc);  /* C with POSIX threads */
    spawn(modulename, myfuncname, [])           % Erlang
    threading.Thread(target=myfunc).start()     # Python with threads
    asyncio.create_task(myfunc())               # Python with asyncio
    

다양한 표기법와 서로 다른 용어가 있겠지만, 문법적으로는 모두 같습니다. 모두 `myfunc`를 프로그램의 나머지 부분과 동시에 실행하려는 것이며, 즉시 돌아와 부모가 나머지 부분을 실행할 수 있도록 하는 것이죠.

다른 방법으로는 콜백을 사용하는 것도 있겠습니다.
    
    
    QObject::connect(&emitter, SIGNAL(event()),        // C++ with Qt
                     &receiver, SLOT(myfunc()))
    g_signal_connect(emitter, "event", myfunc, NULL)   /* C with GObject */
    document.getElementById("myid").onclick = myfunc;  // Javascript
    promise.then(myfunc, errorhandler)                 // Javascript with Promises
    deferred.addCallback(myfunc)                       # Python with Twisted
    future.add_done_callback(myfunc)                   # Python with asyncio
    

다시 한 번, 표현만 다를 뿐 같은 일을 수행합니다. 지금부터 어떤 이벤트가 발생하면 `myfunc`를 실행하라는 것입니다. 한 번 설정되고 나면 즉시 되돌아와 부른 쪽에서 다른 일을 할 수 있게 되죠. (콜백이 [promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all) [combinators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/race), 또는 [Twisted-style protocols/transports](https://twistedmatrix.com/documents/current/core/howto/servers.html)와 같이 그럴싸해 보이는 형태로도 제공됩니다만, 결국 근간은 같습니다.)

그리고... 그렇죠. 실제로 사용되는 일반적인 동시성 API를 생각해보더라도 아마 둘중 한 쪽에 속할 겁니다 (가끔 asyncio와 같이 양쪽에 속하는 경우도 있죠).

하지만 제가 만든 새 라이브러리인 [Trio](https://trio.readthedocs.io)는 좀 다릅니다. 어느 쪽에도 해당되지 않죠. 대신, `myfunc`와 `anotherfunc`를 동시에 실행하고 싶다면, 아래와 같이 하면 됩니다.
    
    
    async with trio.open_nursery() as nursery:
        nursery.start_soon(myfunc)
        nursery.start_soon(anotherfunc)
    

"nursery" 구조를 처음 본 사람이라면 이게 뭔가 싶을껍니다. 왠 들여쓰기가 있나? `nursery` 객체는 또 뭐고, 태스크를 실행하기 위해 왜 이런걸하나? 싶으실 겁니다. 그리고 나서는 다른 프레임워크에서 익숙하게 썼던 패턴을 사용하지 못해 짜증이 나겠죠. 기본 요소라기엔 기이하고 특이하며 너무 상위 수준(high-level)처럼 느껴질 겁니다. 뭐 예상되는 반응입니다! 하지만 좀 참아보세요.

**이 포스트를 통해, 저는 nurseries가 기이하지도 이상하지도 않으며, 반복문이나 함수 호출과 같은 근본적인 새로운 흐름 제어 방식임을 알리고자 합니다. 그리고, 위에서 봤던 기존의 방법 – 쓰레드 복제나 콜백 등록 – 들은 nurseries로 완전히 대체되어야 한다고 봅니다.** 

이상하게 들리나요? 비슷한 일이 예전에도 있었습니다: 바로 `goto`가 흐름 제어의 시작과 끝이던 시절이 있었지만, 이젠 [다 흘러간 얘기](https://xkcd.com/292/)가 된 것 처럼요. 몇몇 언어들이 아직 `goto`라 불리는 것을 가지고 있지만 예전에 `goto`라 불리던 것과 비교하면 다르고 기능이 제한되어 있습니다. 게다가 대부분의 언어에는 아예 없고요. 무슨 일이 있었냐고요? 옛날 옛적 일이라 아는 사람이 별로 없는 이야기지만 놀랄정도로 유사한 이야기입니다. 그럼 이제 `goto`가 어떤 것이었는지 알아보는 걸로 시작해서 그 이야기가 왜 동시성 API에 대한 얘기로 이어지는지 알아봅시다.

**목차:**

  * What is a `goto` statement anyway?
  * What is a `go` statement anyway?
  * What happened to `goto`?
    * `goto`: the destroyer of abstraction
    * A surprise benefit: removing `goto` statements enables new features
    * `goto` statements: not even once
  * `go` statement considered harmful
    * `go` statements: not even once
  * Nurseries: a structured replacement for `go` statements
    * Nurseries preserve the function abstraction.
    * Nurseries support dynamic task spawning.
    * There is an escape.
    * You can define new types that quack like a nursery.
    * No, really, nurseries _always_ wait for the tasks inside to exit.
    * Automatic resource cleanup works.
    * Automated error propagation works.
    * A surprise benefit: removing ` go` statements enables new features
  * Nurseries in practice
  * Conclusion
  * Acknowledgments
  * Footnotes



## 도대체 `goto` 구문이 뭐길래?

자, 역사를 살펴봅시다. 초기의 컴퓨터는 [어셈블리 언어](https://en.wikipedia.org/wiki/Assembly_language)나, 그보다 더 기초적인 수단으로 동작했습니다. 아주 거지같았죠. 1950년대가 되서야 IBM의 [존 배커스](https://en.wikipedia.org/wiki/John_Backus) 나 Remington Rand의 [그레이스 호퍼](https://en.wikipedia.org/wiki/Grace_Hopper) 같은 사람들이 [FORTRAN](https://en.wikipedia.org/wiki/Fortran)과 [FLOW-MATIC](https://en.wikipedia.org/wiki/FLOW-MATIC) (그 후속작인 [COBOL](https://en.wikipedia.org/wiki/COBOL)이 유명하죠)같은 언어를 개발하기 시작했습니다.

이 시기의 FLOW-MATIC은 상당히 비범했습니다. 컴퓨터보다는 사람을 중시한 첫번째 프로그래밍 언어로 파이썬의 할머니의 할아버지의 할머니 정도로 여겨도 됩니다. FLOW-MATIC 코드 맛좀 볼까요.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-1.svg" style="width: 440px;" type="image/svg+xml"> </object>

현대적인 언어와는 다르게 `if`도 없고 반복문이나 함수 호출도 없군요. 알고 보면 블록 구분자와 들여쓰기조차 없습니다. 연속된 구문의 목록일 뿐입니다. 이 프로그램이 단지 짧거나 그럴싸한 제어 문법이 없어서가 아니라, 이 시절엔 아예 블록이라는게 발명되지도 않았기 때문이죠!

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/sequential-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Sequential flow represented as a vertical arrow pointing down, and goto flow represented as an arrow that starts pointing down and then leaps off to the side.</object>

대신 FLOW-MATIC에는 두 가지 제어 방식이 있습니다. 보통은 예상한 대로 위에서 아래로 한 구문씩 순차적으로 실행됩니다. 하지만 `JUMP TO`같은 특별한 구문을 만나면 다른 곳으로 옮겨탑니다. 예를 들어, 구문(13)은 구문(2)로 점프합니다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-2.svg" style="width: 440px;" type="image/svg+xml"> </object>

제가 만든 동시성 기초 요소(역주: nursery)와 마찬가지로, 이 "단방향 점프"를 뭘로 불러야 하는지 논란이 있었습니다. 여기서는 `JUMP TO`라고 했지만, 그 이름은 `goto`로 굳어지게 됩니다. ("go to" 같은거죠) 여기서는 이렇게 부르겠습니다.

자, 이제 이 작은 프로그램의 완전한 `goto` 점프 구성을 봅시다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/flow-matic-4.svg" style="width: 440px;" type="image/svg+xml"> </object>

여러분만 이게 혼돈의 카오스로 보이는건 아닙니다. 이런 식의 점프 기반 프로그래밍은 FLOW-MATIC이 어셈블리 언어로부터 직접적인 영향을 받은 것입니다. 강력하며, 컴퓨터 하드웨어가 동작하는 방식에 딱 맞지만, 직접적으로 사용하기에는 혼란스럽죠. 이 화살표 더미로부터 "스파게티 코드"라는 명칭도 나왔습니다. 더 나은게 반드시 필요합니다.

흠... 이 모든 문제를 일으키는 `goto`란 무엇일까요? 왜 어떤 제어 구문은 괜찮고 어떤건 안될까요? 어떻게 좋은걸 고르죠? 당시에는 이게 명확하지 않기도 해서, 이해하지 못한다면 문제 해결이 정말 어려울 겁니다.

## `go` 구문은?

하지만 잠깐, 모두가 `goto`가 나쁘다고 외치는 역사의 한 순간에 멈춰볼까요? 이 얘기가 동시성과 관련이 있냐고요? 뭐, Golang의 유명한 `go` 구문을 생각해봅시다. 새로운 "goroutine"(경량 쓰레드)을 만들어 보죠.
    
    
    // Golang
    go myfunc();
    

이 흐름을 다이어그램으로 그려볼까요? 음, 위에서 봤던 것과 좀 다릅니다. 흐름이 갈라지니까요. 그림으로 그려보면요,

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/go-schematic-unlabeled.svg" style="width: 395px;" type="image/svg+xml"> "Go" flow represented as two arrows: a green arrow pointing down, and a lavender arrow that starts pointing down and then leaps off to the side.</object>

일부러 _양쪽_ 선의 색상을 다르게 했습니다. 순차적으로 실행될 부모 goroutine(초록선)은 위에서 시작해서 즉시 아래로 진행합니다. 그 동안 자식(라벤더색)은 위에서 시작해서 `myfunc` 본체로 점프합니다. 일반적인 함수 호출과 다르게, 이 점프는 단방향입니다. `myfunc`의 실행은 완전히 새로운 스택에서 이뤄지고, 런타임은 이 실행이 어디에서 시작되었는지도 모릅니다.

이건 Golang에만 해당되는 것은 아닙니다. 이 흐름은 글의 시작에 열거했던 _모든_ 기초 요소에 적용됩니다.

  * 쓰레딩 라이브러리는 일반적으로 나중에 쓰레드를 `join` 할 수 있는 객체를 제공합니다. 하지만 언어 차원에서는 알 수 없는 독립적인 작업입니다. 실제 쓰레드 복제 요소는 위와 같은 제어 흐름을 가집니다.
  * 콜백을 등록하는 것도 문법적으로는 다음과 같은 백그라운드 쓰레드를 시작하는 것과 같습니다. (a) 어떤 일이 발생할 때까지 멈춰있다가, (2) 콜백을 호출합니다. (구현은 완전히 다르게 되겠지만요.) 상위 수준의 흐름 제어로 보자면, 콜백 등록도 `go` 구문과 동일합니다.
  * Future와 promise도 마찬가지입니다. promise를 돌려주는 함수를 호출하는 것은 백그라운드로 일어날 일을 예약한다는 것과 같습니다. 그리고 나중에 join할 객체를 – 원한다면 – 돌려줍니다. 흐름 제어 측면에서 보면, 쓰레드를 생성하는 방식과 같죠. 그리고 promise에 콜백을 등록하는 것이니 두 번 말할 것도 없습니다.

이 같은 패턴이 다양한 형태로 나타납니다. 이 다양한 형태의 핵심은 제어 흐름이 갈라지고, 한 쪽은 단방향으로 점프하고 다른 한 쪽은 호출했던 쪽으로 돌아간다는 것입니다. 뭘 봐야할 지 알게 되면, 같은 것을 여러 곳에서 찾아볼 수 있을겁니다 – 정말 즐거운 일이죠! [^1]

그런데, 이러한 흐름 제어를 부르는 공통된 이름이 없습니다. "`goto` 구문"이 다른 `goto` 같은 구문을 통칭하는 이름이 된 것과 같이, 저도 이런 형태를 모두 "`go` 구문"이라고 부르려고 합니다. 하필 왜 "go" 라고 묻는다면... Golang이 이러한 형태에 대한 명백한 예제가 있달까요. 어쨌든 이제 제가 이걸 가지고 뭘 하려는지 알 것 같은데요. 이 두 다이어그램을 보세요. 비슷하지 않나요?

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/go-schematic-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Repeat of earlier diagrams: goto flow represented as an arrow that starts pointing down and then leaps off to the side, and "go" flow represented as two arrows: a green arrow pointing down, and a lavender arrow that starts pointing down and then leaps off to the side.</object>

맞아요. **go 구문은 goto 구문과 형태가 같습니다.**

동시성 프로그래밍은 작성하고 동작을 추론하기가 어려운 것으로 악명이 높죠. 마치 `goto`-기반 프로그램이 그러했던 것처럼요. 같은 이유로 그렇진 않을까요? 현대 언어들에서는 `goto` 문제가 상당수 해결되었습니다. 우리가 `goto`를 해결한 것과 마찬가지로 이를 통해 사용하기 용이한 동시성 API를 만들어낼 수 있을까요? 한 번 알아봅시다.

## `goto`에 무슨 일이 있었던거야?

당췌 `goto`가 뭐길래 이렇게 많은 문제를 낳았을까요? 1960년대 후반에 [에츠허르 데이크스트라](https://en.wikipedia.org/wiki/Edsger_W._Dijkstra)는 [Go to의 해로움](https://scholar.google.com/scholar?cluster=15335993203437612903&hl=en&as_sdt=0,5)와 [구조적 프로그래밍에 대한 소고](https://www.cs.utexas.edu/~EWD/ewd02xx/EWD249.PDF) (PDF)와 같은, 이 문제를 명확하게 설명하는 요즘 매우 유명해진 글을 남겼습니다.

### `goto`: 추상화의 파괴자

그 문서들에서 데이크스트라는 비순차적 소프트웨어를 작성하고 잘 동작하게 만드는 문제에 대해 우려했습니다. 제가 이러한 통찰에 대해 감히 여기서 평가할 정도가 아니죠. 예를 들자면, 이런 얘기를 들어보셨을 겁니다.

![Testing can be used to show the presence of bugs, but never to show their absence!](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/testing.png)

이건 _구조적 프로그래밍에 대한 소고_ 에서 발췌한 것입니다. 하지만 그는 주로 _추상화_ 에 대해 신경을 썼습니다. 그는 머릿속에 다 담을 수 없을 정도로 거대한 프로그램을 만들고 싶어했습니다. 이를 위해 프로그램의 각 부분을 블랙박스처럼 다룰 필요가 있죠. 파이썬 프로그램을 예로 들어보겠습니다.
    
    
     print("Hello world!")
    

문자열 포매팅, 버퍼 관리, 크로스플랫폼 이슈 등... `print`가 어떻게 구현되어 있는지 알 필요는 없습니다. 그저 당신이 입력한 문자열이 표시될 것이라는 것만 알면 코드의 다른 부분을 작성하는데만 전념할 수 있습니다.  데이크스트라는 이러한 추상화가 프로그래밍 언어 수준에서 제공되길 원했습니다.

이것을 위해, 블록 문법이 발명되었고, ALGOL과 같은 언어에는 5가지 정도의 서로 다른 흐름 제어 구문이 있게 되었습니다. 여전히 순차적으로 실행되고 `goto`도 있었지만요.

앞서 나왔던 순차 진행과 goto 진행을 봅시다.

<object data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/sequential-and-go-to-schematic.svg" style="width: 400px;" type="image/svg+xml"> Same picture of sequential flow and goto flow as before.</object>

그리고 비교문, 반복문, 함수 호출 등이 생겨났죠.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/control-schematics.svg" style="width: 500px;" type="image/svg+xml"> Diagrams with arrows showing the flow control for if statements, loops, and function calls.</object>

You can implement these higher-level constructs using `goto`, and early on, that's how people thought of them: as a convenient shorthand. But what Dijkstra pointed out is that if you look at these diagrams, there's a big difference between `goto` and the rest. For everything except `goto`, flow control comes in the top → [stuff happens] → flow control comes out the bottom. We might call this the "black box rule": if a control structure has this shape, then in contexts where you don't care about the details of what happens internally, you can ignore the [stuff happens] part, and treat the whole thing as regular sequential flow. And even better, this is also true of any code that's _composed_ out of those pieces. When I look at this code:
    
    
     print("Hello world!")
    

I don't have to go read the definition of `print` and all its transitive dependencies just to figure out how the control flow works. Maybe inside `print` there's a loop, and inside the loop there's an if/else, and inside the if/else there's another function call... or maybe it's something else. It doesn't really matter: I know control will flow into `print`, the function will do its thing, and then eventually control will come back to the code I'm reading.

It may seem like this is obvious, but if you have a language with `goto` – a language where functions and everything else are built on top of `goto`, and `goto` can jump anywhere, at any time – then these control structures aren't black boxes at all! If you have a function, and inside the function there's a loop, and inside the loop there's an if/else, and inside the if/else there's a `goto`... then that `goto` could send the control anywhere it wants. Maybe control will suddenly return from another function entirely, one you haven't even called yet. You don't know!

And this breaks abstraction: it means that _every function call is potentially a_ ` goto` _statement in disguise, and the only way to know is to keep the entire source code of your system in your head at once._ As soon as ` goto` is in your language, you stop being able do local reasoning about flow control. That's _why_ ` goto` leads to spaghetti code.

And now that Dijkstra understood the problem, he was able to solve it. Here's his revolutionary proposal: we should stop thinking of if/loops/function calls as shorthands for `goto`, but rather as fundamental primitives in their own rights – and we should remove `goto` entirely from our languages.

From here in 2018, this seems obvious enough. But have you seen how programmers react when you try to take away their toys because they're not smart enough to use them safely? Yeah, some things never change. In 1969, this proposal was _incredibly controversial_. [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth) [defended](https://scholar.google.com/scholar?cluster=17147143327681396418&hl=en&as_sdt=0,5) ` goto`. People who had become experts on writing code with `goto` quite reasonably resented having to basically learn how to program again in order to express their ideas using the newer, more constraining constructs. And of course it required building a whole new set of languages.

![On the left, a photo of a snarling wolf. On the right, a photo of a grumpy bulldog.](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/wolf-and-bulldog.jpg)

Left: A traditional `goto`. Right: A domesticated `goto`, as seen in C, C#, Golang, etc. The inability to cross function boundaries means it can still pee on your shoes, but it probably won't rip your face off.

In the end, modern languages are a bit less strict about this than Dijkstra's original formulation. They'll let you break out of multiple nested structures at once using constructs like `break`, `continue`, or `return`. But fundamentally, they're all designed around Dijkstra's idea; even these constructs that push the boundaries do so only in strictly limited ways. In particular, functions – which are the fundamental tool for wrapping up control flow inside a black box – are considered inviolate. You can't `break` out of one function and into another, and a `return` can take you out of the current function, but no further. Whatever control flow shenanigans a function gets up to internally, other functions don't have to care.

This even extends to `goto` itself. You'll find a few languages that still have something they call `goto`, like C, C#, Golang, ... but they've added heavy restrictions. At the very least, they won't let you jump out of one function body and into another. Unless you're working in assembly [^2], the classic, unrestricted `goto` is gone. Dijkstra won.

### A surprise benefit: removing `goto` statements enables new features

And once `goto` disappeared, something interesting happened: language designers were able to start adding features that depend on control flow being structured.

For example, Python has some nice syntax for resource cleanup: the `with` statement. You can write things like:
    
    
    # Python
    with open("my-file") as file_handle:
        ...
    

and it guarantees that the file will be open during the `...` code, but then closed immediately afterward. Most modern languages have some equivalent (RAII, `using`, try-with-resource, `defer`, ...). And they all assume that control flows in an orderly, structured way. If we used `goto` to jump into the middle of our `with` block... what would that even do? Is the file open or not? What if we jumped out again, instead of exiting normally? Would the file get closed? This feature just doesn't work in any coherent way if your language has `goto` in it.

Error handling has a similar problem: when something goes wrong, what should your code do? Often the answer is to pass the buck up the stack to your code's caller, let them figure out how to deal with it. Modern languages have constructs specifically to make this easier, like exceptions, or other forms of [automatic error propagation](https://doc.rust-lang.org/std/result/index.html#the-question-mark-operator-). But your language can only provide this help if it _has_ a stack, and a reliable concept of  "caller". Look again at the control-flow spaghetti in our FLOW-MATIC program and imagine that in the middle of that it tried to raise an exception. Where would it even go?

### `goto` statements: not even once

So `goto` – the traditional kind that ignores function boundaries – isn't just the regular kind of bad feature, the kind that's hard to use correctly. If it were, it might have survived – lots of bad features have. But it's much worse.

> Even if you don't use `goto` yourself, merely having it as an option in your language makes _everything_ harder to use. Whenever you start using a third-party library, you can't treat it as a black box – you have to go read through it all to find out which functions are regular functions, and which ones are idiosyncratic flow control constructs in disguise. This is a serious obstacle to local reasoning. And you lose powerful language features like reliable resource cleanup and automatic error propagation. Better to remove ` goto` entirely, in favor of control flow constructs that follow the "black box" rule.

## `go` 구문의 해로움

So that's the history of `goto`. Now, how much of this applies to `go` statements? Well... basically, all of it! The analogy turns out to be shockingly exact.

**Go statements break abstraction.** Remember how we said that if our language allows ` goto`, then any function might be a `goto` in disguise? In most concurrency frameworks, `go` statements cause the exact same problem: whenever you call a function, it might or might not spawn some background task. The function seemed to return, but is it still running in the background? There's no way to know without reading all its source code, transitively. When will it finish? Hard to say. If you have `go` statements, then functions are no longer black boxes with respect to control flow. In my [first post on concurrency APIs](https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/), I called this "violating causality", and found that it was the root cause of many common, real-world issues in programs using asyncio and Twisted, like problems with backpressure, problems with shutting down properly, and so forth.

**Go statements break automatic resource cleanup.** Let's look again at that ` with` statement example:
    
    
    # Python
    with open("my-file") as file_handle:
        ...
    

Before, we said that we were "guaranteed" that the file will be open while the `...` code is running, and then closed afterwards. But what if the `...` code spawns a background task? Then our guarantee is lost: the operations that _look_ like they're inside the ` with` block might actually keep running _after_ the ` with` block ends, and then crash because the file gets closed while they're still using it. And again, you can't tell from local inspection; to know if this is happening you have to go read the source code to all the functions called inside the `...` code.

If we want this code to work properly, we need to somehow keep track of any background tasks, and manually arrange for the file to be closed only when they're finished. It's doable – unless we're using some library that doesn't provide any way to get notified when the task is finished, which is distressingly common (e.g. because it doesn't expose any task handle that you can join on). But even in the best case, the unstructured control flow means the language can't help us. We're back to implementing resource cleanup by hand, like in the bad old days.

**Go statements break error handling.** Like we discussed above, modern languages provide powerful tools like exceptions to help us make sure that errors are detected and propagated to the right place. But these tools depend on having a reliable concept of  "the current code's caller". As soon as you spawn a task or register a callback, that concept is broken. As a result, every mainstream concurrency framework I know of simply gives up. If an error occurs in a background task, and you don't handle it manually, then the runtime just... drops it on the floor and crosses its fingers that it wasn't too important. If you're lucky it might print something on the console. (The only other software I've used that thinks "print something and keep going" is a good error handling strategy is grotty old Fortran libraries, but here we are.) Even Rust – the language voted Most Obsessed With Threading Correctness by its high school class – is guilty of this. If a background thread panics, Rust [discards the error and hopes for the best](https://doc.rust-lang.org/std/thread/).

Of course you _can_ handle errors properly in these systems, by carefully making sure to join every thread, or by building your own error propagation mechanism like [errbacks in Twisted](https://twistedmatrix.com/documents/current/core/howto/defer.html#visual-explanation) or [Promise.catch in Javascript](https://hackernoon.com/promises-and-error-handling-4a11af37cb0e). But now you're writing an ad-hoc, fragile reimplementation of the features your language already has. You've lost useful stuff like "tracebacks" and "debuggers". All it takes is forgetting to call ` Promise.catch` once and suddenly you're dropping serious errors on the floor without even realizing. And even if you do somehow solve all these problems, you'll still end up with two redundant systems for doing the same thing.

### `go` statements: not even once

Just like `goto` was the obvious primitive for the first practical high-level languages, `go` was the obvious primitive for the first practical concurrency frameworks: it matches how the underlying schedulers actually work, and it's powerful enough to implement any other concurrent flow pattern. But again like `goto`, it breaks control flow abstractions, so that merely having it as an option in your language makes everything harder to use.

The good news, though, is that these problems can all be solved: Dijkstra showed us how! We need to:

  * Find a replacement for `go` statements that has similar power, but follows the "black box rule",
  * Build that new construct into our concurrency framework as a primitive, and don't include any form of `go` statement.



And that's what Trio did.

## Nurseries: `go`를 대체하는 구조적 용법

Here's the core idea: every time our control splits into multiple concurrent paths, we want to make sure that they join up again. So for example, if we want to do three things at the same time, our control flow should look something like this:

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-schematic-unlabeled.svg" style="width: 250px;" type="image/svg+xml"> </object>

Notice that this has just one arrow going in the top and one coming out the bottom, so it follows Dijkstra's black box rule. Now, how can we turn this sketch into a concrete language construct? There are some existing constructs that meet this constraint, but (a) my proposal is slightly different than all the ones I'm aware of and has advantages over them (especially in the context of wanting to make this a standalone primitive), and (b) the concurrency literature is vast and complicated, and trying to pick apart all the history and tradeoffs would totally derail the argument, so I'm going to defer that to a separate post. Here, I'll just focus on explaining my solution. But please be aware that I'm not claiming to have like, invented the idea of concurrency or something, this draws inspiration from many sources, I'm standing on the shoulders of giants, etc. [^3]

Anyway, here's how we're going to do it: first, we declare that a parent task cannot start any child tasks unless it first creates a place for the children to live: a _nursery_. It does this by opening a _nursery block_ ; in Trio, we do this using Python's `async with` syntax:

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-1-pathified.svg" style="width: 350px;" type="image/svg+xml"> </object>

Opening a nursery block automatically creates an object representing this nursery, and the `as nursery` syntax assigns this object to the variable named `nursery`. Then we can use the nursery object's `start_soon` method to start concurrent tasks: in this case, one task calling the function `myfunc`, and another calling the function `anotherfunc`. Conceptually, these tasks execute _inside_ the nursery block. In fact, it's often convenient to think of the code written inside the nursery block as being an initial task that's automatically started when the block is created.

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-2-pathified.svg" style="width: 500px;" type="image/svg+xml"></object>

Crucially, the nursery block doesn't exit until all the tasks inside it have exited – if the parent task reaches the end of the block before all the children are finished, then it pauses there and waits for them. The nursery automatically expands to hold the children.

Here's the control flow: you can see how it matches the basic pattern we showed at the beginning of this section:

<object class="align-center" data="https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/nursery-3-pathified.svg" style="width: 600px;" type="image/svg+xml"> </object>

This design has a number of consequences, not all of which are obvious. Let's think through some of them.

### Nurseries preserve the function abstraction.

The fundamental problem with `go` statements is that when you call a function, you don't know whether it's going to spawn some background task that keeps running after it's finished. With nurseries, you don't have to worry about this: any function can open a nursery and run multiple concurrent tasks, but the function can't return until they've all finished. So when a function does return, you know it's really done.

### Nurseries support dynamic task spawning.

Here's a simpler primitive that would also satisfy our flow control diagram above. It takes a list of thunks, and runs them all concurrently:
    
    
    run_concurrently([myfunc, anotherfunc])
    

But the problem with this is that you have to know up front the complete list of tasks you're going to run, which isn't always true. For example, server programs generally have `accept` loops, that take incoming connections and start a new task to handle each of them. Here's a minimal `accept` loop in Trio:
    
    
    async with trio.open_nursery() as nursery:
        while True:
            incoming_connection = await server_socket.accept()
            nursery.start_soon(connection_handler, incoming_connection)
    

With nurseries, this is trivial, but implementing it using `run_concurrently` would be _much_ more awkward. And if you wanted to, it would be easy to implement ` run_concurrently` on top of nurseries – but it's not really necessary, since in the simple cases `run_concurrently` can handle, the nursery notation is just as readable.

### There is an escape.

The nursery object also gives us an escape hatch. What if you really do need to write a function that spawns a background task, where the background task outlives the function itself? Easy: pass the function a nursery object. There's no rule that only the code directly inside the `async with open_nursery()` block can call `nursery.start_soon` – so long as the nursery block remains open [^4], then anyone who acquires a reference to the nursery object gets the capability of spawning tasks into that nursery. You can pass it in as a function argument, send it through a queue, whatever.

In practice, this means that you can write functions that "break the rules", but within limits:

  * Since nursery objects have to be passed around explicitly, you can immediately identify which functions violate normal flow control by looking at their call sites, so local reasoning is still possible.
  * Any tasks the function spawns are still bound by the lifetime of the nursery that was passed in.
  * And the calling code can only pass in nursery objects that it itself has access to.



So this is still very different from the traditional model where any code can at any moment spawn a background task with unbounded lifetime.

One place this is useful is in the proof that nurseries have equivalent expressive power to `go` statements, but this post is already long enough so I'll leave that for another day.

### You can define new types that quack like a nursery.

The standard nursery semantics provide a solid foundation, but sometimes you want something different. Perhaps you're envious of Erlang and its supervisors, and want to define a nursery-like class that handles exceptions by restarting the child task. That's totally possible, and to your users, it'll look just like a regular nursery:
    
    
    async with my_supervisor_library.open_supervisor() as nursery_alike:
        nursery_alike.start_soon(...)
    

If you have a function that takes a nursery as an argument, then you can pass it one of these instead to control the error-handling policy for the tasks it spawns. Pretty nifty. But there is one subtlety here that pushes Trio towards different conventions than asyncio or some other libraries: it means that `start_soon` has to take a function, not a coroutine object or a `Future`. (You can call a function multiple times, but there's no way to restart a coroutine object or a `Future`.) I think this is the better convention anyway for a number of reasons (especially since Trio doesn't even have `Future`s!), but still, worth mentioning.

### No, really, nurseries _always_ wait for the tasks inside to exit.

It's also worth talking about how task cancellation and task joining interact, since there are some subtleties here that could – if handled incorrectly – break the nursery invariants.

In Trio, it's possible for code to receive a cancellation request at any time. After a cancellation is requested, then the next time the code executes a "checkpoint" operation ([details](https://trio.readthedocs.io/en/latest/reference-core.html#checkpoints)), a `Cancelled` exception is raised. This means that there's a gap between when a cancellation is _requested_ and when it actually _happens_ – it might be a while before the task executes a checkpoint, and then after that the exception has to unwind the stack, run cleanup handlers, etc. When this happens, the nursery always waits for the full cleanup to happen. We _never_ terminate a task without giving it a chance to run cleanup handlers, and we _never_ leave a task to run unsupervised outside of the nursery, even if it's in the process of being cancelled.

### Automatic resource cleanup works.

Because nurseries follow the black box rule, they make `with` blocks work again. There's no chance that, say, closing a file at the end of a `with` block will accidentally break a background task that's still using that file.

### Automated error propagation works.

As noted above, in most concurrency systems, unhandled errors in background tasks are simply discarded. There's literally nothing else to do with them.

In Trio, since every task lives inside a nursery, and every nursery is part of a parent task, and parent tasks are required to wait for the tasks inside the nursery... we _do_ have something we can do with unhandled errors. If a background task terminates with an exception, we can rethrow it in the parent task. The intuition here is that a nursery is something like a  "concurrent call" primitive: we can think of our example above as calling `myfunc` and `anotherfunc` at the same time, so our call stack has become a tree. And exceptions propagate up this call tree towards the root, just like they propagate up a regular call stack.

There is one subtlety here though: when we re-raise an exception in the parent task, it will start propagating in the parent task. Generally, that means that the parent task will exit the nursery block. But we've already said that the parent task cannot leave the nursery block while there are still child tasks running. So what do we do?

The answer is that when an unhandled exception occurs in a child, Trio immediately cancels all the other tasks in the same nursery, and then waits for them to finish before re-raising the exception. The intuition here is that exceptions cause the stack to unwind, and if we want to unwind past a branch point in our stack tree, we need to unwind the other branches, by cancelling them.

This does mean though that if you want to implement nurseries in your language, you may need some kind of integration between the nursery code and your cancellation system. This might be tricky if you're using a language like C# or Golang where cancellation is usually managed through manual object passing and convention, or (even worse) one that doesn't have a generic cancellation mechanism.

### A surprise benefit: removing `go` statements enables new features

Eliminating `goto` allowed previous language designers to make stronger assumptions about the structure of programs, which enabled new features like `with` blocks and exceptions; eliminating `go` statements has a similar effect. For example:

  * Trio's cancellation system is easier to use and more reliable than competitors, because it can assume that tasks are nested in a regular tree structure; see [Timeouts and cancellation for humans](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/) for a full discussion.
  * Trio is the only Python concurrency library where control-C works the way Python developers expect ([details](https://vorpus.org/blog/control-c-handling-in-python-and-trio/)). This would be impossible without nurseries providing a reliable mechanism for propagating exceptions.



## Nurseries를 써보자

So that's the theory. How's it work in practice?

Well... that's an empirical question: you should try it and find out! But seriously, we just won't know for sure until lots of people have pounded on it. At this point I'm pretty confident that the foundation is sound, but maybe we'll realize we need to make some tweaks, like how the early structured programming advocates eventually backed off from eliminating `break` and `continue`.

And if you're an experienced concurrent programmer who's just learning Trio, then you should expect to find it a bit rocky at times. You'll have to [learn new ways to do things](https://stackoverflow.com/questions/48282841/in-trio-how-can-i-have-a-background-task-that-lives-as-long-as-my-object-does) – just like programmers in the 1970s found it challenging to learn how to write code without `goto`.

But of course, that's the point. As Knuth wrote ([Knuth, 1974](https://scholar.google.com/scholar?cluster=17147143327681396418&hl=en&as_sdt=0,5), p. 275):

> Probably the worst mistake any one can make with respect to the subject of **go to** statements is to assume that  "structured programming" is achieved by writing programs as we always have and then eliminating the **go to** 's. Most **go to** 's shouldn't be there in the first place! What we really want is to conceive of our program in such a way that we rarely even _think_ about **go to** statements, because the real need for them hardly ever arises. The language in which we express our ideas has a strong influence on our thought processes. Therefore, Dijkstra asks for more new language features – structures which encourage clear thinking – in order to avoid the **go to** 's temptations towards complications.

And so far, that's been my experience with using nurseries: they encourage clear thinking. They lead to designs that are more robust, easier to use, and just better all around. And the limitations actually make it easier to solve problems, because you spend less time being tempted towards unnecessary complications. Using Trio has, in a very real sense, taught me to be a better programmer.

For example, consider the Happy Eyeballs algorithm ([RFC 8305](https://tools.ietf.org/html/rfc8305)), which is a simple concurrent algorithm for speeding up the establishment of TCP connections. Conceptually, the algorithm isn't complicated – you race several connection attempts against each other, with a staggered start to avoid overloading the network. But if you look at [Twisted's best implementation](https://github.com/twisted/twisted/compare/trunk...glyph:statemachine-hostnameendpoint), it's almost 600 lines of Python, and still has [at least one logic bug](https://twistedmatrix.com/trac/ticket/9345). The equivalent in Trio is more than **15x** shorter. More importantly, using Trio I was able to write it in minutes instead of months, and I got the logic correct on my first try. I never could have done this in any other framework, even ones where I have much more experience. For more details, you can [watch my talk at Pyninsula last month](https://www.youtube.com/watch?v=i-R704I8ySE). Is this typical? Time will tell. But it's certainly promising.

## 결론

The popular concurrency primitives – `go` statements, thread spawning functions, callbacks, futures, promises, ... they're all variants on `goto`, in theory and in practice. And not even the modern domesticated `goto`, but the old-testament fire-and-brimstone `goto`, that could leap across function boundaries. These primitives are dangerous even if we don't use them directly, because they undermine our ability to reason about control flow and compose complex systems out of abstract modular parts, and they interfere with useful language features like automatic resource cleanup and error propagation. Therefore, like `goto`, they have no place in a modern high-level language.

Nurseries provide a safe and convenient alternative that preserves the full power of your language, enables powerful new features (as demonstrated by Trio's cancellation scopes and control-C handling), and can produce dramatic improvements in readability, productivity, and correctness.

Unfortunately, to fully capture these benefits, we do need to remove the old primitives entirely, and this probably requires building new concurrency frameworks from scratch – just like eliminating `goto` required designing new languages. But as impressive as FLOW-MATIC was for its time, most of us are glad that we've upgraded to something better. I don't think we'll regret switching to nurseries either, and Trio demonstrates that this is a viable design for practical, general-purpose concurrency frameworks.

## 붙임

Many thanks to Graydon Hoare, Quentin Pradet, and Hynek Schlawack for comments on drafts of this post. Any remaining errors, of course, are all my fault.

Credits: Sample FLOW-MATIC code from [this brochure](http://archive.computerhistory.org/resources/text/Remington_Rand/Univac.Flowmatic.1957.102646140.pdf) (PDF), as [preserved by the Computer History Museum](http://www.computerhistory.org/collections/catalog/102646140). [Wolves in Action](https://www.flickr.com/photos/iam_photo/478178221), by i:am. photography / Martin Pannier, licensed under [CC-BY-SA 2.0](https://creativecommons.org/licenses/by-nc-sa/2.0/), cropped. [French Bulldog Pet Dog](https://pixabay.com/en/french-bulldog-pet-dog-funny-2427629/) by Daniel Borker, released under the [CC0 public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).

## 각주

[^1]: At least for a certain kind of person.  
[^2]: And WebAssembly even demonstrates that it's possible and at least somewhat desirable have a low-level assembly language without `goto`: [reference](https://www.w3.org/TR/wasm-core-1/#control-instructions%E2%91%A0), [rationale](https://github.com/WebAssembly/design/blob/master/Rationale.md#control-flow)  
[^3]: For those who can't possibly pay attention to the text without first knowing whether I'm aware of their favorite paper, my current list of topics to include in my review are: the "parallel composition" operator in Cooperating/Communicating Sequential Processes and Occam, the fork/join model, Erlang supervisors, Martin Sústrik's article on [Structured concurrency](http://250bpm.com/blog:71) and work on [libdill](https://github.com/sustrik/libdill), and [crossbeam::scope](https://docs.rs/crossbeam/0.3.2/crossbeam/struct.Scope.html) / [rayon::scope](https://docs.rs/rayon/1.0.1/rayon/fn.scope.html) in Rust. Edit: I've also been pointed to the highly relevant [golang.org/x/sync/errgroup](https://godoc.org/golang.org/x/sync/errgroup) and [github.com/oklog/run](https://godoc.org/github.com/oklog/run) in Golang. If I'm missing anything important, [let me know](mailto:njs@pobox.com).  
[^4]: If you call `start_soon` _after_ the nursery block has exited, then ` start_soon` raises an error, and conversely, if it doesn't raise an error, then the nursery block is guaranteed to remain open until the task finishes. If you're implementing your own nursery system then you'll want to handle synchronization carefully here.  
