title: What I've learned about accessibility in SPAs
author: Nolan Lawson
source: https://nolanlawson.com/2019/11/05/what-ive-learned-about-accessibility-in-spas/

## What I've learned about accessibility in SPAs

Over the past year or so, I've learned a lot about accessibility, mostly thanks to working on [Pinafore](https://pinafore.social), which is a Single Page App (SPA). In this post, I'd like to share some of the highlights of what I've learned, in the hope that it can help others who are trying to learn more about accessibility.

One big advantage I've had in this area is the help of [Marco Zehe](https://marcozehe.wordpress.com/), an accessibility expert who works at Mozilla and is blind himself. Marco has patiently coached me on a lot of these topics, and [his comments on the Pinafore GitHub repo](https://github.com/nolanlawson/pinafore/issues?q=is%3Aissue+author%3Amarcozehe+is%3Aclosed) are a treasure trove of knowledge.

So without further ado, let's dive in!

## Misconceptions

One misconception I've observed in the web community is that JavaScript is somehow inherently anti-accessibility. This seems to stem from a time when [screen readers did not support JavaScript particularly well](https://www.brucelawson.co.uk/2011/javascript-and-screenreaders/), and so indeed the more JavaScript you used, the more likely things were to be inaccessible.

I've found, though, that most of the accessibility fixes I've made have actually involved writing _more_ JavaScript, not less. So today, this rule is definitely more myth than fact. However, there are a few cases where it holds true:

### divs and spans versus buttons and inputs

Here's the best piece of accessibility advice for newbies: if something is a button, make it a `<button>`. If something is an input, make it an `<input>`. Don't try to reinvent everything from scratch using `<div>`s and `<span>`s. This may seem obvious to more seasoned web developers, but for those who are new to accessibility, it's worth reviewing why this is the case.

First off, for anyone who doubts that this is a thing, there was a large open-source dependency of Pinafore (and of Mastodon) that had several thousand GitHub stars, tens of thousands of weekly downloads on npm, and was composed almost entirely of `<div>s` and `<span>`s. In other words: when something should have been a `<button>`, it was instead a `<span>` with a `click` listener. (I've since fixed most of these accessibility issues, but this was the state I found it in.)

This is a real problem! People really do try to build entire interfaces out of `<div>`s and `<span>`s. Rather than chastise, though, let me analyze the problem and offer a solution.

I believe the reason people are tempted to use `<div>`s and `<span>`s is that they have minimal user agent styles, i.e. there is less you have to override in CSS. However, resetting the style on a `<button>` is actually pretty easy:


    button {
      margin: 0;
      padding: 0;
      border: none;
      background: none;
    }


99% of the time, I've found that this was all I needed to reset a `<button>` to have essentially the same style as a `<div>` or a `<span>`. For more advanced use cases, you can explore [this CSS Tricks article](https://css-tricks.com/overriding-default-button-styles/).

In any case, the whole reason you want to use a real `<button>` over a `<span>` or a `<div>` is that you essentially get accessibility for free:

  * For keyboard users who `Tab` around instead of using a mouse, a `<button>` automatically gets the right focus in the right order.
  * When focused, you can press the `Space` bar on a `<button>` to press it.
  * Screen readers announce the `<button>` as a button.
  * Etc.



You _could_ build all this yourself in JavaScript, but you 'll probably mess something up, and you'll also have a bunch of extra code to maintain. So it's best just to use the native semantic HTML elements.

### SPAs must manually handle focus and scroll position

There is another case where the "JavaScript is anti-accessibility" mantra has a kernel of truth: SPA navigation. Within SPAs, it's common for JavaScript to handle navigation between pages, i.e. by modifying the DOM and [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API) rather than triggering a full page load. This causes several challenges for accessibility:

  * You need to manage focus yourself.
  * You need to manage scroll position yourself.



For instance, let's say I'm in my timeline, and I want to click this timestamp to see the full thread of a post:

![Screenshot of Pinafore timeline showing a post from me with an arrow pointing to the timestamp](https://nolanwlawson.files.wordpress.com/2019/11/screenshot_2019-11-02-toot-cafe-c2b7-profile.png?w=570&h=358)

When I click the link and then press the back button, focus should return to the element I last clicked (note the purple outline):

![Screenshot showing the same image as above, but with a focus outline around the timestamp](https://nolanwlawson.files.wordpress.com/2019/11/screenshot_2019-11-02-toot-cafe-c2b7-profile2.png?w=570&h=355)

For classic server-rendered pages, most browser engines [^1] give you this functionality for free. You don't have to code anything. But in an SPA, since you're overriding the normal navigation behavior, you have to handle the focus yourself.

This also applies to scrolling, especially in a virtual list. In the above screenshot, note that I'm scrolled down to exactly the point in the page from before I clicked. Again, this is seamless when you're dealing with server-rendered pages, but for SPAs the responsibility is yours.

## Easier integration testing

One thing I was surprised to learn is that, by making my app more accessible, I also made it easier to test. Consider the case of toggle buttons.

A [toggle button](https://www.w3.org/TR/wai-aria-practices-1.1/#button) is a button that can have two states: pressed or not pressed. For instance, in the screenshot below, the "boost" and "favorite" buttons (i.e. the circular arrow and the star) are toggle buttons, because it's possible to boost or favorite a post, and they start off in unboosted/unfavorited states.

[![Screenshot of a Mastodon post in Pinafore with the favorite \(star\) button pressed and the boost button unpressed](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-02-13-38-01-1.png?w=570&h=215)](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-02-13-38-01-1.png)

Visually, there are plenty of styles you can use to signal the pressed/unpressed state - for instance, I've opted to make the colors darker when pressed. But for the benefit of screen reader users, you'll typically want to use a pattern like the following:


    <button type="button" aria-pressed="false">
      Unpressed
    </button>
    <button type="button" aria-pressed="true">
      Pressed
    </button>


Incidentally, this makes it easier to write integration tests (e.g. using [TestCafe](https://devexpress.github.io/testcafe/) or [Cypress](https://www.cypress.io/)). Why rely on classes and styles, which might change if you redesign your app, when you can instead rely on the semantic attributes, which are guaranteed to stay the same?

I observed this pattern again and again: the more I improved accessibility, the easier things were to test. For instance:

  * When using the [feed pattern](https://www.w3.org/TR/wai-aria-practices-1.1/#feed), I could use `aria-posinset` and `aria-setsize` to confirm that the virtual list had the correct number of items and in the correct order.
  * For buttons without text, I could test the `aria-label` rather than the background image or something that might change if the design changed.
  * For hidden elements, I could use `aria-hidden` to identify them.
  * Etc.



So make accessibility a part of your testing strategy! If something is easy for screen readers to interpret, then it'll probably be easier for your automated tests to interpret, too. After all, screen reader users might not be able to see colors, but neither can your headless browser tests!

## Subtleties with focus management

After watching [this talk by Ian Forrest](https://youtu.be/pNcB7ChyO1E) and [playing around with KaiOS](https://nolanlawson.com/2019/09/22/the-joy-and-challenge-of-developing-for-kaios/), I realized I could make some small changes to improve keyboard accessibility in my app.

As pointed out in the talk, it's not necessarily the case that every mouse-accessible element also needs to be keyboard-accessible. If there are redundant links on the page, then you can skip them in the `tabindex` order, so a keyboard user won't have to press `Tab` so much.

In the case of Pinafore, consider a post. There are two links that lead to the user's profile page - the profile picture and the user name:

![Screenshot showing a Mastodon post with red rectangles around the user avatar and the user name](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-11-55-25.png?w=570&h=123)

These two links lead to exactly the same page; they are strictly redundant. So I chose to add `tabindex="-1"` to the profile picture, giving keyboard users one less link to have to `Tab` through. Especially on a KaiOS device with a tiny d-pad, this is a nice feature!




In the above video, note that the profile picture and timestamp are skipped in the tab order because they are redundant - clicking the profile picture does the same thing as clicking the user name, and clicking the timestamp does the same thing as clicking on the entire post. (Users can also disable the "click the entire post" feature, as [it may be problematic for those with motor impairments](https://github.com/nolanlawson/pinafore/issues/163). In that case, the timestamp is re-added to the tab order.)

Interestingly, an element with `tabindex="-1"` can still become focused if you click it and then press the back button. But luckily, tabbing _out_ of that element does the right thing as long as the other tabbable elements are in the proper order.

## The final boss: accessible autocomplete

After implementing several accessible widgets from scratch, including the feed pattern and an image carousel (which I described [in a previous post](https://nolanlawson.com/2019/02/10/building-a-modern-carousel-with-css-scroll-snap-smooth-scrolling-and-pinch-zoom/)), I found that the single most complicated widget to implement correctly was autocompletion.




Originally, [I had implemented this widget](https://github.com/nolanlawson/pinafore/issues/129) by following [this design](https://haltersweb.github.io/Accessibility/autocomplete.html), which relies largely on creating an element with `aria-live="assertive"` which explicitly speaks every change in the widget state (e.g. "the current selected item is number 2 of 3"). This is kind of a heavy-handed solution, though, and it led to [several bugs](https://github.com/nolanlawson/pinafore/issues/1512).

After toying around with a few patterns, I eventually settled on a more standard design using [aria-activedescendant](https://www.w3.org/TR/wai-aria-1.1/#aria-activedescendant). Roughly, the HTML looks like this:


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


Explaining this pattern probably deserves a blog post in and of itself, but in broad strokes, what's happening is:

  * The description and label are offscreen, using [styles which make it only visible to screen readers](https://github.com/nolanlawson/pinafore/blob/af1bb984c93a4961c12ab92001519a18af963cc0/src/scss/global.scss#L185-L195). The description explains that you can press up or down on the results and press enter to select.
  * `aria-expanded` indicates whether there are autocomplete results or not.
  * `aria-activedescendant` indicates which option in the list is selected.
  * `aria-label`s on the options allow me to control how it's spoken to a screen reader, and to explicitly include text like "1 of 2" in case the screen reader doesn't speak this information.



After extensive testing, this was more-or-less the best solution I could come up with. It works perfectly in NVDA on the latest version of Firefox, although sadly [it has some minor issues in VoiceOver on Safari and NVDA on Chrome](https://github.com/nolanlawson/pinafore/pull/1513#issue-320087960). However, since this is the standards-based solution (and doesn't rely on `aria-live="assertive"` hacks), my hope is that browsers and screen readers will catch up with this implementation.

## Manual and automated accessibility testing

There are a lot of automated tools that can give you good tips on improving accessibility in your web app. Some of the ones I've used include [Lighthouse](https://developers.google.com/web/tools/lighthouse/) (which uses [Axe](https://www.deque.com/axe/) under the hood), the [Chrome accessibility tools](https://developers.google.com/web/tools/chrome-devtools/accessibility/reference), and the [Firefox accessibility tools](https://hacks.mozilla.org/2019/10/auditing-for-accessibility-problems-with-firefox-developer-tools/). (These tools can give you slightly different results, so I like to use multiple so that I can get second opinions!)

[![Screenshot of a post in Pinafore with the Firefox accessibility tools open in a side panel](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-08-37-50.png?w=570&h=290)](https://nolanwlawson.files.wordpress.com/2019/11/screenshot-from-2019-11-03-08-37-50.png)

However, I've found that, especially for screen reader accessibility, there is no substitute for testing in an actual browser with an actual screen reader. It gives you the exact experience that a screen reader user would have, and it helps build empathy for what kinds of design patterns work well for voice navigation and which ones don't. Also, sometimes screen readers have bugs or slightly differing behavior, and these are things that accessibility auditing tools can't tell you.

If you're just getting started, I would recommend watching [Rob Dodson's "A11ycasts" series](https://www.youtube.com/playlist?list=PLNYkxOF6rcICWx0C9LVWWVqvHlYJyqw7g), especially the tutorials on [VoiceOver for macOS](https://youtu.be/5R-6WvAihms) and [NVDA for Windows](https://youtu.be/Jao3s_CwdRU). (Note that NVDA is usually paired with Firefox and VoiceOver is optimized for Safari. So although you can use either one with other browsers, those are the pairings that tend to be [most representative of real-world usage](https://webaim.org/projects/screenreadersurvey8/).)

Personally I find VoiceOver to be the easiest to use from a developer's point of view, mostly because it has a visual display of the assistive text while it's being spoken.

[![Screenshot of VoiceOver in Safari on macOS showing text at the bottom of the screen representing what's spoken](https://nolanwlawson.files.wordpress.com/2019/11/screen-shot-2019-11-03-at-9.00.38-am.png?w=570&h=312)](https://nolanwlawson.files.wordpress.com/2019/11/screen-shot-2019-11-03-at-9.00.38-am.png)

NVDA can also be configured to do this, but you have to know to go into the settings and enable the ["Speech Viewer" option](https://www.nvaccess.org/files/nvda/documentation/userGuide.html#SpeechViewer). I would definitely recommend turning this on if you're using NVDA for development!

[![Screenshot of Speech Viewer in NVDA on Firefox showing lines of text representing what's spoken](https://nolanwlawson.files.wordpress.com/2019/11/2019-11-03-08_56_18-greenshot.png?w=570&h=322)](https://nolanwlawson.files.wordpress.com/2019/11/2019-11-03-08_56_18-greenshot.png)

Similar to testing screen readers, it's also a good idea to try `Tab`ing around your app to see how comfortable it is with a keyboard. Does the focus change unexpectedly? Do you have to do a lot of unnecessary `Tab`ing to get where you want? Are there any handy keyboard shortcuts you'd like to add?

For a lot of things in accessibility, there are no hard-and-fast rules. Like design or usability in general, sometimes you just have to experience what your users are experiencing and see where you can optimize.

## Conclusion

Accessibility can be challenging, but ultimately it's worth the effort. Working on accessibility has improved the overall usability of my app in a number of ways, leading to unforeseen benefits such as [KaiOS arrow key navigation](https://github.com/nolanlawson/arrow-key-navigation/) and better integration tests.

The greatest satisfaction, though, comes from users who are happy with the work I've done. I was beyond pleased when Marco had this to say:

> "Pinafore is for now by far the most accessible way to use Mastodon. I use it on desktop as well as iOS, both iPhone & iPad, too. So thank you again for getting accessibility in right from the start and making sure the new features you add are also accessible."
>  – [Marco Zehe, October 21 2019](https://toot.cafe/@marcozehe/103001716835941254)

Thank you, Marco, and thanks for all your help! Hopefully this blog post will serve as a way to pay your accessibility advice forward.

_Thanks to Sorin Davidoi, Thomas Wilburn, and Marco Zehe for feedback on a draft of this post._

[^1] In the course of writing this article, I was surprised to learn that, for server-rendered pages, pressing the back button restores focus to the previously-clicked element in Firefox, Safari, and Edge (EdgeHTML), but _not_ Chrome. I found [a webcompat.com bug](https://webcompat.com/issues/28121) describing the browser difference, I've gone ahead and filed [a bug on Chrome](https://bugs.chromium.org/p/chromium/issues/detail?id=1020915).
