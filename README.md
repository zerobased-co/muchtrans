# muchtrans

[![Netlify Status](https://api.netlify.com/api/v1/badges/ccfc9531-b5eb-41b6-8e00-7fe9c7fa14a1/deploy-status)](https://app.netlify.com/sites/muchtrans/deploys)

Muchtrans is yet another translation platform, under heavy developement.

## Why muchtrans?

I've translated English articles into Korean for years. During translation processes, I found the importance of showing original contents with translated paragraphs. It helps readers to find out wrong translations and makes them work together for better translations. By reading original contents side-by-side, you can improve your language skills at the same time either.

So, I made it like this.

The second reason is recording translators and their contribution in clear way. Text files could be well tracked by Git so I chose it as a tracker. By using Git, we can get a free lunch benefits from its toolchain and eco systems like GitHub. We can track down the translation history only by reading Git commit history.

## To add an article

If you're familiar with Git and GitHub, then create a pull request with a new article(e.g. `new_article.md`) and the translation file(e.g. `new_article.ko.md`) within `articles` directory. [Netlify](https://netlify.com) will build it automatically and generate intermediate site for verification. 
You can build in your local by running `python build.py`. It generates HTML files within `_build` directory.

Or, just leave a URL with some explanation why it should be translated on [GitHub Issue](https://github.com/zerobased-co/muchtrans/issues/9).

## To build muchtrans

On your Python environments,

```shell
$ pip install -r requirements.txt
$ python build.py
$ cd _build
$ python -m http.server
```
And connect to `http://localhost:8000` in your favour web browser.

## License

Original articles may have their own license. Translated articles can be published under `MIT license` as same as muchtrans codes.
