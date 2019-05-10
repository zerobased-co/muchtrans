title: Color accessibility: tools and resources to help you design inclusive products
author: Stéphanie Walter
source: https://stephaniewalter.design/blog/color-accessibility-tools-resources-to-design-inclusive-products/

# Color accessibility: tools and resources to help you design inclusive products

I wrote a [quick tweet about teaching the basics of accessibility and colors to design students](https://twitter.com/WalterStephanie/status/1111960235491639296) that go quite some attention. It brought up some interesting discussions on color accessibility (also discussions I didn’t expect about emojis ^^). So I thought I would share with you all the resources, tips and tools I regularly use to build and check the color accessibility of my products in one place. Enjoy.

## Contrasts and accessibility: a few basics on color

When building products (digital ones but this could also apply to other products), color choice is important. The color can convey your brand identity, help users understand information, etc. Unfortunately, **not everybody gets to experience colors the same way**. Some users might be **color blind** , some users might be **visually impaired** , some users might be in different environments. This is why you need to **be careful about accessibility** when you are using color in your products.

I will not enter in all the details since I’m no accessibility expert. What you need to understand about accessibility is that there’s a list of criterion you can find under the [WCAG 2.1 guidelines](https://www.w3.org/TR/WCAG21) to help you. For this small introduction, I will stick to the **AA criteria**. Those look scary, a little bit like the HTML specification, I know. In this big list, [the 1.4 section](https://www.w3.org/TR/WCAG21/#use-of-color) is dedicated to “making it easier for users to see and hear content including separating foreground from background.”

So for accessibility and colors, there’s 2 big things you need to remember:

  1.  **Don’t use color as the only visual means of conveying an information** , action, etc.
  2.  **Ensure sufficient contrast ratio between foreground** (text or icons but this also now applied to form borders and other elements) **and their background.**

![The 2 criteria explained visually](https://stephaniewalter.design/wp-content/uploads/2019/04/2main-coloraccessibility-rules.jpg)

For the first criteria, it means for instance that if you create a graph, you should have some secondary way of helping people understand the different sections. [Trello has a nice example for that](https://wearecolorblind.com/examples/trello-colorblind-friendly-mode/). If you have a form, you can’t just use a red border to show there’s an error. There’s more example on the[ Understanding Success Criterion 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html) page.

For the second criteria, it means that the contrast between text (or foreground elements) and color should be:

  *  **4.5 to 1** for text **smaller than 18 points** and **smaller than 14 points if bold**
  *  **3 to 1 f** or text **bigger than 18 points** and **at least 14 points if bold**

The conversion points > pixels isn’t super simple but if you want more details you can check [Understanding Success Criterion 1.4.3: Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

Basically: **small text under 24px** (or bold text under 19px) **need to follow the 4.5 rule** , **bigger text over 24px** (or bold text over 19px) **need to follow the 3 ratio rule.**

Okay, so now you might wonder “but how am I supposed to measure this 4.5 or 3 contrast ratio, do I need to do maths for each color combination?!”. Don’t worry, I have a selection of tools and resources to help you get started.

## Color blindness simulators tools

The first criteria is about **making sure that the information isn’t only conveyed by color**. You can of course start by checking your mockups and hunt down any places where this criteria can be applied. Forms, infographics, graphs, tags, statuses are usually a good place to start. Also, product colors pickers if you are doing an e-commerce website (more about that in the articles in next section). Then, you can use color blindness simulators to check your color choice against different types of color blindness.

[ **Color Oracle** ](https://colororacle.org/)is a free colorblind simulator that works for Windows, Mac and Linux.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/colorblindsimulator-oracle.jpg)

 **[Stark](https://getstark.co/)** is a Sketch plugin that will let you simulate different types of color blindness.

 _If you are using Photoshop, you can go to View > Proof Setup and chose one of the color blind options_

![](https://stephaniewalter.design/wp-content/uploads/2019/04/colorblindsimulator-stark-sketch.jpg)

 **[Toptal’s colorfilter](https://www.toptal.com/designers/colorfilter) ** online tool lets you test your website and shows you how people with different color blindness will see your pages

![](https://stephaniewalter.design/wp-content/uploads/2019/04/colorblindsimulator-toptal.jpg)

## Tools to help you check color contrast

The second criteria is **the contrast ratio between text (or foreground elements) and background**. As I told you here, you won’t need to do the maths yourself, there’s plenty of tools to help you with that.

### Online tools

[Tanaguru Contrast Finder](http://contrast-finder.tanaguru.com/) not only lets you check the contrast ratio between two colors, it also helps you find a new color if the one you chose didn’t match the desired contrast ratio. You can learn more about that in my article [Tips to Create an Accessible and Contrasted Color Palette](https://stephaniewalter.design/blog/tips-create-accessible-color-palette/).

![](https://stephaniewalter.design/wp-content/uploads/2019/04/tanaguru.jpg)

[ **Color Review**](https://color.review/check/FEDC2A-5A3B5D) lets you check the contrast ratio between two colors. It shows you a preview of what the color combination would look like. The picker on the left helps you find an alternative if the colors you picked won't work.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/color-review.jpg)

 **[Contrast Ratio](https://contrast-ratio.com/)** is an online tool that will check the text color against the background and will show you the result and the ratio in simple and efficient way
 
![](data:image/gif;base64,R0lGODdhAQABAPAAAP///wAAACwAAAAAAQABAEACAkQBADs=)![](https://stephaniewalter.design/wp-content/uploads/2019/04/contrast-ratio.jpg)

 **[Colorable](http://jxnblk.com/colorable/demos/text/?background=%23123409&foreground=%23DACDCD)** is another online tool that will let you check text/background contrast ratio. I like this one because you can enter the text color, the background one, preview what it will look like. Then if the contrast ratio isn’t high enough you can play with the little Hue, Saturation and Lightness levers to find a color that will work.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/colorable.jpg)

If you want to test a whole site you can use [Checkmycolours.com](http://www.checkmycolours.com/) this tools lets you enter a URL and will then create a report of all the contrast issues if found on your site. Be careful with the results though, sometimes it has issues grabbing the right background.

### Offline tools you want to install

[Contrast Analyser](https://developer.paciellogroup.com/resources/contrastanalyser/) is THE tool you can install on Windows, macOS and Linux. It lets you grab a color with the color picker and check the contrast ratio. I would be careful with the picker though, depending on my screen setup I sometimes had issues and the hexadecimal it grabbed wasn’t exactly the right one, so for now I stick to “copy pasting” hexadecimal colors in the tool.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/color-contrast-analyser.jpg)

If you are on mac and willing to pay $7 you can get [usecontrast.com](https://usecontrast.com/), but I haven’t tested it.

## Color accessibility in product design: articles and resources

Now that you have some tools, here are a few more articles and resources to help you get started and build accessible products.

### Building an accessible color palette

 **[90 combinations](http://clrs.cc/a11y/) ** is a page that shows, well, hum, 90 combination of text/background color that are have sufficient contrast ratio. Be careful about the ratio though, some of those have a 4.1 AA large ratio which means you can only use them for text bigger than 18pt (or bold text bigger than 14pt). If you lack inspiration, this site a place to starts, but…

But from a designer perspective, I think that you might want to avoid half of the 90 combinations. Purple on yellow or green on violet might pass the 4.5 ratio, but they are still super annoying to read. Just because you can doesn’t mean you should!

![](https://stephaniewalter.design/wp-content/uploads/2019/04/90accessible-color-combinations.jpg)

 **[Accessible color palette builder](https://toolness.github.io/accessible-color-matrix/?n=white&n=Color%202&n=Color%203&n=Color%204&n=Color%205&v=FFFFFF&v=FEDC2A&v=5A3B5D&v=8B538F&v=C3A3C9) ** is one of my favorite tool. You can enter up to 6 colors and it will build you this color matrix and let you know what colors can be combined.

![](data:image/gif;base64,R0lGODdhAQABAPAAAP///wAAACwAAAAAAQABAEACAkQBADs=)![](https://stephaniewalter.design/wp-content/uploads/2019/04/color-matrix-accessibility.jpg)

This one is limited to 6 colors, if you want a more complex matrix with more colors you can [check this tool as well](http://jxnblk.com/colorable/demos/matrix/).

[ **Contrast Grid**](http://contrast-grid.eightshapes.com/?background-colors=%23FFFFFF%2C%20White%0D%0A%23FEDC2A%2C%20Yellow%0D%0A%235A3B5D%2C%20Dark%20Purple%0D%0A%238B538F%2C%20Light%20Purple%0D%0A%23C3A3C9%2C%20Lightst%20purple%0D%0A%23777777%2C%20Gray%0D%0A%23555555%2C%20Darker%20Gray%0D%0A%0D%0A&foreground-colors=%23FFFFFF%2C%20White%0D%0A%23FEDC2A%2C%20Yellow%0D%0A%235A3B5D%2C%20Dark%20Purple%0D%0A%238B538F%2C%20Light%20Purple%0D%0A%23C3A3C9%2C%20Lightst%20purple%0D%0A%23777777%2C%20Gray%0D%0A%23555555%2C%20Darker%20Gray%0D%0A%23444444%2C%20Darker%20%20Darker%20Gray%0D%0A%23333333%2C%20Fifty%20Shades%20of%20darker%20gray%0D%0A%23222222%2C%20Dorian%20Gray%3F&es-color-form__tile-size=regular) takes this concept of a grid of foreground and background combos and brings it to the next level. In this tool you can chose what specific colors you want for lines and columns and build your own custom grid (via [MickaÃ«l G.](https://twitter.com/StrapTrooper))

![](data:image/gif;base64,R0lGODdhAQABAPAAAP///wAAACwAAAAAAQABAEACAkQBADs=)![](https://stephaniewalter.design/wp-content/uploads/2019/04/contrast-grid.jpg)

 **[Cloudflare color tool](https://cloudflare.design/color/) ** Okay, this one is NOT the most intuitive tool but it’s super powerful. At the top of the screen you can choose to build a palette from a URL, an image or play with the color box. Then you get a list of colors you can use. Drag and drop those colors in the 4 categories (parent, color, background and border) to get a nice preview, or use the “view 4 accessible combinations” link to see accessible color combinations.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/cloudfour-contrast-tool.jpg)

[My struggle with colors - Demystifying colors for accessible digital experiences](https://uxdesign.cc/my-struggle-with-colors-52156c664b87) and [My struggle with colors, part II - Building an accessible color system from scratch.](https://uxdesign.cc/my-struggle-with-colors-part-ii-ed71bff6302a) I applied the method of the 10 shades with the 5-steps method on a few projects, it works quite well.

### Helping color blind users understand your content

[We are Colorblind](https://wearecolorblind.com/) is a website with ressource, articles and examples dedicated to help other people understand color blindness.

![](https://stephaniewalter.design/wp-content/uploads/2019/04/wearecolorblind.jpg)

  * [Designing UI with Color Blind Users in Mind](https://www.secretstache.com/blog/designing-for-color-blind-users/) 7 tips to help you design for color blind users, from patterns and textures to symbols, labels, etc.
  * [Color Blindness Considerations for Designers and Content Managers](https://medium.com/@sheribyrnehaber/color-blindness-considerations-for-designers-and-content-managers-a767ab38a825?ref=heydesigner), some quick tips to help you design for color blind people
  * [5 Ways to Improve Your Ecommerce Design for Colourblind Users](https://www.shopify.com/partners/blog/86314118-5-ways-to-improve-your-ecommerce-design-for-colourblind-users), this one is specific for ecommerce, which brings its own issues of “how am I supposed to chose a tshirt if I can’t make the difference between the colors on the screen”
  * [Colorblind accessibility in video games – is the industry heading in the right direction?](http://www.gamersexperience.com/colorblind-accessibility-in-video-games-is-the-industry-heading-in-the-right-direction/) An interesting article in the game industry where color blindness plays a big role for some games

### Geri Coady’s ressources

Geri Coady is an amazing designer who put a lot of resources out there to help you:

  * [Color Accessibility Workflows](https://abookapart.com/products/color-accessibility-workflows) the book at a book appart
  * She also wrote [A Pocket Guide To Colour Accessibility](http://hellogeri.com/blog/view/now_available_pocket_guide_to_colour_accessibility) but it seems complicated to find now
  * [Colour Accessibility](https://24ways.org/2012/colour-accessibility/), the basics on 24 ways

### A few more articles to help

Finally, here a few more articles with some tips to go a little bit deeper in this topic

  * [A guide to color accessibility in product design](https://www.invisionapp.com/inside-design/color-accessibility-product-design/) another nice article to help you get started
  * [Color in Design Systems 16 Tips for Setting Up a System That Endures](https://medium.com/eightshapes-llc/color-in-design-systems-a1c80f65fa3), tips 13 to 16 are all about accessibility
  * [Color Contrast for Better Readability](https://www.viget.com/articles/color-contrast/) an article to help you establish and use an accessible color palette.
  * [Chrome DevTools: Accessible Colors](https://uxdesign.cc/chrome-devtools-accessible-colors-300ec462a63c)

If you have more tools and ressources to share, the comments are open.

### Help, I'm stuck with the client's branding

Sometimes, you have to work with client branding. Some of them won't like it if you tell them that you want to change their corporate color because of contrast issues on the website. For those cases, a last solution is to [**use a style switcher to provide a conforming alternate version**](https://www.w3.org/TR/WCAG-TECHS/C29.html).

 _Also thank you [Geoffrey Crofte](https://twitter.com/geoffreycrofte) for the proof reading and adding one tool to the list _ 🙂

Are you looking for a UX or UI designer, for a site or mobile application? Do you want me to give a talk at your conference, or simply want to know more about me? You can take a look at [my portfolio](https://stephaniewalter.design/#work) and contact me.
