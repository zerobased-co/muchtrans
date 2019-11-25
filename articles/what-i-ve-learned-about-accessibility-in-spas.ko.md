title: SPA에서의 접근성에 대해 배운 것들
author: Nolan Lawson
source: https://nolanlawson.com/2019/11/05/what-ive-learned-about-accessibility-in-spas/

## SPA에서의 접근성에 대해 배운 것들

지난 일 년간, 단일 페이지 앱(Single Page App, 이하 SPA)인 [Pinafore](https://pinafore.social)를 만들며 감사하게도 접근성에 대해 많은 것을 배울 수 있었습니다. 이 글을 통해 그간 배운 것들 중 중요한 것들을 공유하며, 접근성을 배우고자 하는 이들에게 도움이 되었으면 좋겠습니다.

이 분야를 경험하며 시각장애인이며, 모질라에서 접근성 전문가로 일하고 있는 [Marco Zehe](https://marcozehe.wordpress.com/)에게 많은 도움을 받았습니다. Marco는 인내심을 가지고 여러 가지 주제에 대해 저를 지도해주었으며, [그가 Pinafore 깃헙 리포지터리에 남긴 글](https://github.com/nolanlawson/pinafore/issues?q=is%3Aissue+author%3Amarcozehe+is%3Aclosed)들은 지식의 보고라고 봐도 무방할 정도입니다.

고민만 하지 말고, 일단 살펴봅시다!

## 오해

웹 커뮤니티에서 흔히 발견할 수 있는 오해 중 하나는 자바스크립트가 근본적으로 접근성에 해가 된다는 의견입니다. 이는 아마도 [스크린 리더가 자바스크립트를 잘 지원하지 않을 때](https://www.brucelawson.co.uk/2011/javascript-and-screenreaders/) 생기고, 실제로 자바스크립트를 많이 쓰면 쓸수록 그런 경향이 있긴 합니다.

하지만 대부분의 접근성 문제를 해결하는 과정에서 저는 실제로 더 *많은* 자바스크립트를 작성해야 했습니다. 그러니까 요즘은, 이 얘기는 사실이라기보다는 미신에 가깝습니다. 그럼에도 몇 가지 경우에는 여전히 맞는 말이기도 합니다.

### &lt;div&gt; &amp; &lt;span&gt; vs &lt;button&gt; &amp; &lt;input&gt;

초보자들에게 접근성과 관련된 가장 유용한 내용을 알려드리겠습니다: 버튼 같은 것은 그냥 `<button>`으로 만드세요. 입력을 받아야 한다면 `<input>`으로 만들고요. `<div>`나 `<span>`을 이용해서 모든 걸 바닥부터 새로 만들려고 하지 마세요. 노련한 웹 개발자들에겐 자명한 문제로 보이겠지만, 접근성을 처음 다뤄보는 분들은 왜 이렇게 해야 하는지 알아두면 좋겠네요.

이게 이렇게 말할 거리나 되나 싶은 분들에게 설명드리자면, Pinafore(그리고 Mastodon도 마찬가지로)이 의존하고 있는 수많은 오픈소스들 – 대부분 GitHub에서 수천 개 이상의 스타를 받았고, npm의 주간 다운로드가 수십만 회가 넘는 프로젝트들임에도 – 거의 전체가 `<div>`와 `<span>`으로 이루어져 있었습니다. 즉, `<button>`이어야 했던 것들이 `<span>`에 `click` 리스너가 붙은 체로 있었다는 얘깁니다. (그 이후로 이런 접근성 이슈를 대부분 고쳤지만, 제가 발견한 당시에는 그랬었습니다.)

이거 진짜 문제 아닐까요?! 사람들은 전체 인터페이스를 `<div>`와 `<span>` 덩어리로 만들려 하고 있어요. 하지만 비난만 하지 않고, 원인을 찾아 해결책을 제안해보고자 합니다.

`<div>`와 `<span>`이 브라우저 기본 스타일(user agent style)이 가장 적어, CSS에서 재정의할 값이 별로 없는 점 때문에 널리 사용된다고 생각합니다. 하지만 `<button>`의 스타일을 초기화하는 것도 그리 어렵지 않습니다.

```css
button {
  margin: 0;
  padding: 0;
  border: none;
  background: none;
}
```

대부분의 경우에 이것만으로도 `<button>`의 스타일을 기본적으로 `<div>`나 `<span>`과 같도록 초기화할 수 있었습니다. 몇몇 특별한 경우에 대해서는 [this CSS Tricks article](https://css-tricks.com/overriding-default-button-styles/)에서 확인해보세요.

어쨌든, `<span>`이나 `<div>`가 아닌 진짜 `<button>`을 사용해야 하는 근본적인 이유는 다음의 접근성 개선을 거저 얻을 수 있기 때문입니다.

  * 마우스 대신 키보드의 `Tab`을 사용하는 사람에게, `<button>`에 포커스를 올바른 순서로 제공할 수 있습니다.
  * 포커스를 가졌을 때, `<button>` 위에서 `Space`를 눌러 선택할 수 있습니다.
  * 스크린 리더가 `<button>`을 버튼으로 알려줄 수 있습니다.
  * 등등.



이 모든 걸 직접 JavaScript로 구현하는 것도 *가능*은 하지만, 어딘가에서 실수하거나 추가로 유지 보수해야 하는 코드가 늘어날 겁니다. 그러니까 기본으로 제공되는 의미 있는 HTML 요소를 쓰는 것이 좋겠습니다.

### SPA는 포커스와 스크롤 위치를 반드시 수동으로 다뤄야 한다

“자바스크립트는 접근성에 반한다”는 격언이 지닌 진실된 핵심이 적용되는 경우가 있습니다: 바로 SPA 내비게이션이죠. SPA 상에서, 자바스크립트를 통해 페이지를 전환하는 것은 일반적입니다. 페이지 전체를 새로 불러오는 대신에 DOM을 조작하고 [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API)를 이용하는 식이죠. 이런 방식은 접근성 측면에서 몇 가지 문제를 가져옵니다.

  * 포커스를 직접 관리해야 합니다.
  * 스크롤 위치를 직접 관리해야 합니다.



제 타임라인에서 타임스탬프를 클릭해서 해당 포스트의 전체 타래를 보고자 하는 경우를 예로 들어봅시다.

![제가 쓴 포스트의 타임스탬프를 커서로 가리키고 있는 Pinafore 타임라인의 스크린샷](https://nolanwlawson.files.wordpress.com/2019/11/screenshot_2019-11-02-toot-cafe-c2b7-profile.png?w=570&h=358)

링크를 클릭하고, 뒤로 가기 버튼을 누르면 제가 마지막으로 클릭했던 버튼에 포커스가 있어야 합니다(보라색 외곽선을 보세요).

![위와 같은 이미지이지만, 타임스탬프 주위로 포커스 외곽선이 있는 스크린샷](https://nolanwlawson.files.wordpress.com/2019/11/screenshot_2019-11-02-toot-cafe-c2b7-profile2.png?w=570&h=355)

전통적인 서버 측에서 렌더링되는 페이지에서는, 대부분의 브라우저 엔진[^1]이 이 기능을 공짜로 제공해줍니다. 아무것도 코딩할 필요가 없죠. 하지만 SPA에서는 일반적인 내비게이션 행동을 재정의한 상황이므로, 포커스를 스스로 다뤄야 합니다.

이는 스크롤할 때도 적용되는데요, 특히 가상의 리스트<sup>(역주: 무한히 스크롤되는)</sup>에서 그렇습니다. 위의 스크린샷에서 보면, 제가 클릭했을 때와 정확하게 같은 위치로 스크롤되어 있음을 알 수 있습니다. 다시 말하지만, 이건 서버 측 렌더링을 할 경우에만 해당되는 얘기고, SPA에서는 여러분에게 그 책임이 있습니다.

## 통합 테스트가 쉬워집니다

제 앱의 접근성을 향상시키면서 놀라운 것을 하나 배웠는데, 이를 통해 테스트가 더 쉬워진다는 것이었습니다. 토글 버튼의 경우를 예로 들어볼게요.

[토글 버튼](https://www.w3.org/TR/wai-aria-practices-1.1/#button)은 눌렸거나, 눌리지 않은 두 가지 상태를 가질 수 있습니다. 아래 스크린샷에서 “boost”와 “favorite” 버튼(재귀 화살표와 별 모양)은 토글 버튼인데요, 포스트를 부스트 하거나 즐겨찾기 할 수 있는데, 둘 다 부스트 하지 않고/즐겨찾기 하지 않은 상태로 시작하기 때문입니다.

[![눌려 있는 별 버튼과 눌리지 않은 부스트 버튼을 가진 Pinafore에 게시된 Mastodon 포스트](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-02-13-38-01-1.png?w=570&h=215)](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-02-13-38-01-1.png)

눌리고/눌리지 않은 상태를 시각적으로 표현하는 방법은 다양합니다. 저는 눌렸을 때 더 어두운 색을 사용하도록 하기도 했습니다. 하지만 스크린 리더 사용자들을 고려한다면, 일반적으로 다음과 같은 패턴을 선택할 겁니다.

```html
<button type="button" aria-pressed="false">
  Unpressed
</button>
<button type="button" aria-pressed="true">
  Pressed
</button>
```

놀랍게도, 이렇게 함으로써 통합 테스트를 작성하기가 더 쉬워졌습니다. ([TestCafe](https://devexpress.github.io/testcafe/)나 [Cypress](https://www.cypress.io/)에서요) 앱을 다시 디자인할 때 달라질 수도 있는 클래스나 스타일에 의존하기보다는, 동일함이 보장되는 의미(semantic)를 속성으로 가지는 쪽에 의존하는 편이 낫지 않을까요?

이런 패턴을 계속해서 발견했습니다. 제가 접근성을 개선하면 할수록, 테스트하기는 더 쉬워졌습니다. 예를 들면,

  * [피드 패턴](https://www.w3.org/TR/wai-aria-practices-1.1/#feed)을 사용하면서 `aria-posinset`과 `aria-setsize`를 이용해 가상 리스트가 올바른 아이템의 수와 순서를 유지하는지 확인했습니다.
  * 문자열이 없는 버튼을 테스트할 때, 디자인이 달라지면 바뀔 수 있는 배경 이미지나 다른 것을 사용하는 대신 `aria-label`를 사용할 수 있었습니다.
  * 숨겨진 요소에 대해서 `aria-hidden`으로 확인했습니다.
  * 등등.



그러므로, 접근성 향상을 테스팅의 전략으로 삼아보세요! 스크린 리더가 해석하기에 쉽다면, 아마 자동화된 테스트가 해석하기에도 쉬울 것입니다. 스크린 리더 사용자가 색상을 볼 수 없는 것처럼, 헤드리스 브라우저(headless browser) 테스트도 마찬가지일테니까요.

## 포커스 관리의 미묘함

[Ian Forrest의 발표](https://youtu.be/pNcB7ChyO1E)와 [playing around with KaiOS](https://nolanlawson.com/2019/09/22/the-joy-and-challenge-of-developing-for-kaios/)를 보고, 제 앱에서 작은 변경사항 만으로도 키보드 접근성에 대한 향상을 가져올 수 있음을 알았습니다.

발표에서 지적한 것과 같이, 마우스로 접근할 수 있는 모든 요소에 대해 키보드로 접근하게 만들 필요는 없습니다. 꼭 필요한 링크가 아니라면 `tabindex` 순서에서 제외시켜, 키보드 사용자가 `Tab`을 지나치게 많이 누르지 않도록 할 수도 있습니다.

Pinafore의 경우에는 각 포스트에 사용자 프로필 페이지로 이동하는 두 개의 링크가 있습니다. 프로필 사진과 사용자 이름이죠.

![Mastodon 포스트에 있는 사용자 아바타와 사용자 이름에 빨간 테두리가 쳐져 있는 스크린샷](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-11-55-25.png?w=570&h=123)

두 링크는 같은 페이지로 연결되어 있으므로 꼭 둘 다 있을 필요는 없습니다. 그래서 프로필 사진에 `tabindex="-1"`을 적용해서 키보드 사용자가 `Tab`을 한 번 덜 누를 수 있도록 했습니다. [KaiOS](https://en.wikipedia.org/wiki/KaiOS) 장치와 같이 작은 다이얼 패드를 가진 경우에 특히 좋을 겁니다!


<video autostart="no" muted="yes" loop="no" preload="auto" playsinline="" controls=""><source src="https://videos.files.wordpress.com/6Ve9dla5/kazam_screencast_00005_dvd.mp4" type="video/mp4"></video>


위 영상을 통해 프로필 사진과 타임스탬프는 탭 순서에서 제외되어 있음을 확인할 수 있습니다. 프로필 사진을 누르는 것은 사용자 이름을 누르는 것과 같고, 타임스탬프는 전체 포스트를 누르는 것과 같아 불필요하기 때문입니다. ([운동 장애가 있는 사람에게는 문제가 될 수 있으므로](https://videos.files.wordpress.com/6Ve9dla5/kazam_screencast_00005_dvd.mp4) “전체 포스트 클릭하기”도 비활성화할 수 있습니다. 이 경우에는 타임스탬프가 탭 순서에 다시 포함됩니다.)

`tabindex="-1"`을 가진 요소를 클릭한 다음 뒤로 돌아오면 포커스가 가능하다는 것이 이상하긴 하지만, 탭으로 이동 가능한 다른 요소들이 올바른 순서로 있는 한, 그 요소에서 탭으로 *나온* 뒤에는 제대로 동작해서 다행입니다.

## 최종 보스: 자동 완성에 대한 접근성

피드 패턴이나 이미지 캐러셀 등 ([이전 포스트](https://nolanlawson.com/2019/02/10/building-a-modern-carousel-with-css-scroll-snap-smooth-scrolling-and-pinch-zoom/)에서 설명했던) 몇몇 접근성 위젯을 바닥부터 만들어가며, 올바르게 구현하기 가장 어려운 요소 중 하나가 자동완성임을 알게 되었습니다.


<video autostart="no" muted="yes" loop="no" preload="auto" playsinline="" controls=""><source src="https://videos.files.wordpress.com/VjC1fOLq/kazam_screencast_00002_dvd.mp4" type="video/mp4"></video>


처음에는 모든 상태 변경에 대해 – “현재 선택된 아이템은 세 가지 중 두 번째입니다”와 같이 — 말하는 `aria-live="assertive"` 속성을 가진 요소를 만드는 것에 상당히 의존하는 [이 디자인](https://haltersweb.github.io/Accessibility/autocomplete.html)을 따라 [이런 위젯을 구현](https://github.com/nolanlawson/pinafore/issues/129)했었습니다. 한 땀 한 땀 수작업으로 해결하는 방법이라 결국 [다양한 버그](https://github.com/nolanlawson/pinafore/issues/1512)가 나올 수밖에 없었습니다.

몇 가지 패턴을 시험해본 후, 최종적으로 [aria-activedescendant](https://www.w3.org/TR/wai-aria-1.1/#aria-activedescendant)를 사용하는 표준 디자인을 선택했습니다. HTML은 대략 이렇게 생겼습니다.

```html
<textarea
  id="the-textarea"
  aria-describedby="the-description"
  aria-owns="the-list"
  aria-expanded="false"
  aria-autocomplete="both"
  aria-activedescendant="option-1">
</textarea>
<ul id="the-list" role="listbox">
  <li
    id="option-1"
    role="option"
    aria-label="First option (1 of 2)">
  </li>
  <li
    id="option-2"
    role="option"
    aria-label="Second option (2 of 2)">
  </li>
</ul>
<label for="the-textarea" class="sr-only">
  What's on your mind?
</label>
<span id="the-description" class="sr-only">
  When autocomplete results are available, press up or down
  arrows and enter to select.
</span>
```

이를 설명하기 위해 따로 글을 써야 할 수준이지만, 대략적으로 이렇게 동작한다고 볼 수 있습니다.

  * 설명과 라벨은 [스크린 리더에서만 보이는 스타일](https://github.com/nolanlawson/pinafore/blob/af1bb984c93a4961c12ab92001519a18af963cc0/src/scss/global.scss#L185-L195)을 사용해서 화면에서는 보이지 않게 합니다. 이를 통해 위아래 키를 눌러 엔터로 선택할 수 있음을 알려줍니다.
  * `aria-expanded`는 자동완성 결과 여부를 알려줍니다.
  * `aria-activedescendant`는 목록에서 어떤 옵션을 골랐는지 알려줍니다.
  * 옵션에 있는 `aria-label`을 통해 스크린 리더가 정보를 말하지 않을 경우, “두 개중 첫 번째”와 같이 명확하게 스크린 리더가 어떤 문자열을 포함해서 읽어야 하는지 제어할 수 있습니다.



광범위한 테스팅 끝에, 이게 덜하지도 더하지도 않는, 제가 할 수 있는 최선의 방법임을 알았습니다. 최신 버전의 파이어폭스의 [NVDA](https://en.wikipedia.org/wiki/NonVisual_Desktop_Access) 하에서 완벽하게 동작합니다. 비록 [사파리의 보이스오버(VoiceOver)와 크롬의 NVDA에서는 문제]((https://github.com/nolanlawson/pinafore/pull/1513#issue-320087960)가 있지만요. 이 방법이 `aria-live="assertive"` 핵에 의존하지 않는 표준에 기반판 방법이므로, 브라우저와 스크린 리더가 이 구현을 제대로 할 날을 기다립니다.

**수정**: 크롬+NVDA와 사파리+보이스오버에서도 이 위젯이 동작하도록 했습니다. 변경사항은 [이 댓글](https://github.com/nolanlawson/pinafore/pull/1632#issuecomment-552154682)에서 확인해보세요.

## 수동 및 자동화된 접근성 테스트

웹 앱의 접근성을 개선하기 위한 좋은 팁을 알려주는 다양한 자동화 도구들이 있습니다. 저도 사용하는 [Lighthouse](https://developers.google.com/web/tools/lighthouse/)(내부적으로 [Axe](https://www.deque.com/axe/)를 사용하죠)라던가 [크롬 접근성 도구](https://developers.google.com/web/tools/chrome-devtools/accessibility/reference), 그리고 [파이어폭스 접근성 도구](https://hacks.mozilla.org/2019/10/auditing-for-accessibility-problems-with-firefox-developer-tools/)들이 있습니다. (도구들마다 조금씩 다른 결과를 제시하니, 저는 다양한 의견을 얻기 위해 여러 도구를 사용하는 편입니다!)

[![파이어폭스 접근성 도구를 옆 패널에 열어둔 Pinafore 포스트의 스크린샷](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-08-37-50.png?w=570&h=290)](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-08-37-50.png)

그런데, 특히 스크린 리더 접근성에 대해서는 스크린 리더로는 실제 브라우저에서의 테스트를 대체할 수 없다는 것을 알았습니다. 스크린 리더 사용자가 가질만한 경험을 정확하게 제공할 뿐 아니라 어떤 디자인 패턴이 음성 내비게이션과 잘 동작하며 어떤 것은 그렇지 않을 지에 대한 공감을 이끌어내는데 도움을 줍니다. 스크린 리더는 버그가 있어 종종 다른 행동을 하기도 하는데, 이런 것들은 접근성 감사 도구에서는 확인할 수 없는 부분입니다.

갓 시작한 분이라면, [Rob Dodson의 “A11ycasts” 시리즈](https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g) 중 [VoiceOver for macOS](https://youtu.be/5R-6WvAihms)과 [NVDA for Windows](https://youtu.be/Jao3s_CwdRU)에 대한 튜토리얼 시청을 추천합니다. (NVDA는 파이어폭스에, 보이스오버는 사파리에 더 최적화돼있음을 유의하세요. 다른 조합으로도 사용할 수는 있지만, 이 조합이 [실제로 가장 많이 사용](https://webaim.org/projects/screenreadersurvey8/)되고 있습니다.)


개인적으로 개발자의 입장에서 사용하기 가장 편리했던 도구는 말하는 내용을 도움 문자열(assistive text)로 보여주는 보이스오버였습니다.

[![macOS의 사파리에서 무엇을 말했는지 화면의 하단에 문자열로 보여주는 보이스오버의 스크린샷](https://nolanwlawson.files.wordpress.com/2019/11/screen-shot-2019-11-03-at-9.00.38-am.png?w=570&h=312)](https://nolanwlawson.files.wordpress.com/2019/11/screen-shot-2019-11-03-at-9.00.38-am.png)

NVDA도 이렇게 동작하도록 할 수 있지만, 설정에 들어가 [“Speech Viewer” 옵션](https://www.nvaccess.org/files/nvda/documentation/userGuide.html#SpeechViewer)을 활성화해야 합니다. 만약 NVDA 개발자가 이 글을 보고 있다면 켜있는 것을 기본값으로 해주었으면 좋겠어요!

[![Screenshot of Speech Viewer in NVDA on Firefox showing lines of text representing what's spoken](https://nolanwlawson.files.wordpress.com/2019/11/2019-11-03-08_56_18-greenshot.png?w=570&h=322)](https://nolanwlawson.files.wordpress.com/2019/11/2019-11-03-08_56_18-greenshot.png)

스크린 리더를 테스트하는 것과 비슷하게, 여러분의 앱에서 `Tab`을 눌러보며 키보드로 얼마나 편하게 사용할 수 있는지 알아보는 것도 좋습니다. 포커스가 의도치 않게 달라졌나요? 원하는 곳에 가기 위해서 `Tab`을 불필요하게 많이 눌러야 하나요? 사용하기에 편리하도록 추가하고 싶은 키보드 단축키가 있나요?

접근성에 대한 많은 것들에 반드시 해야 할(hard-and-fast) 규칙이란 없습니다. 디자인이나 사용성에 대한 얘기와 마찬가지로, 사용자가 어떤 경험을 하고 있고 어디를 최적화해야 하는지 실제로 직접 경험해야 합니다.

## 결론

접근성은 도전적이지만, 궁극적으로 노력을 들일 만한 일입니다. 다양한 방법으로 접근성을 향상시키기 위해 노력하다 보면 [KaiOS의 방향키 내비게이션](https://github.com/nolanlawson/arrow-key-navigation/)과 같은 예상치 못했던 개선과 더 나은 통합 테스트로 나아갈 수 있습니다.

그리고 가장 큰 보람은, 제가 했던 작업으로 행복한 사용자들에게서 옵니다. Marco에게 이런 얘기를 들었을 때 더할 나위 없이 기뻤습니다.

> “Mastodon을 사용하기 위한 가장 접근성 높은 방법은 바로 Pinafore입니다. 저는 데스크톱뿐만 아니라 아이폰과 아이패드의 iOS에서도 같이 사용하고 있습니다. 개발 초기부터 접근성을 중요하게 생각하고, 계속해서 새로운 기능을 접근성 있게 만들어주신 것에 감사드립니다.”
>  – [Marco Zehe, 2019년 10월 21일](https://toot.cafe/@marcozehe/103001716835941254)

Marco, 당신의 도움이 진심으로 감사드립니다! 여러분에게도 이 글이 접근성에 대해 한 걸음 나아갈 수 있는 도움이 되기를 빕니다.

*이 글에 피드백을 주신 Sorin Davidoi, Thomas Wilburn, 그리고 Marco Zehe에게 감사합니다.*

[^1]: 이 글을 쓰는 와중에, 서버 측 렌더링을 하는 경우에 뒤로 가기 버튼을 누르면 이전에 클릭했던 포커스가 복원된다는 것을 알고 놀랬습니다. 크롬을 제외한 파이어폭스, 사파리, 엣지(EdgeHTML)에서 동작합니다. [a webcompat.com bug](https://webcompat.com/issues/28121)에서 브라우저 차이점에 대한 설명을 발견하고, [크롬에 버그를 제보](https://bugs.chromium.org/p/chromium/issues/detail?id=1020915)했습니다.
