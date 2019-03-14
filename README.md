# muchtrans

[![Netlify Status](https://api.netlify.com/api/v1/badges/ccfc9531-b5eb-41b6-8e00-7fe9c7fa14a1/deploy-status)](https://app.netlify.com/sites/muchtrans/deploys)

Muchtrans is yet another translation platform, under heavy developement.
<br>Muchtrans는 한창 개발하고 있는 또 다른 번역 플랫폼입니다.

## Why muchtrans? / 왜 muchtrans 인가요?

I've translated English articles into Korean for years. During translation processes, I found the importance of showing original contents with translated paragraphs. It helps readers to find out wrong translations and makes them work together for better translations. By reading original contents side-by-side, you can improve your language skills at the same time either.
<br>지난 몇 년간 영어 문서를 한국어로 번역해왔습니다. 번역하는 과정에서 원본 콘텐츠를 번역된 것과 함께 보여주는 것의 중요성을 파악했습니다. 이를 통해 독자가 잘못된 번역을 쉽게 찾을 수 있도록 하고 함께 더 나은 번역을 가능하게 합니다. 원본 콘텐츠를 함께 읽으므로 외국어 실력도 동시에 향상시킬 수 있습니다.

So, I made it like this.
<br>그래서 이렇게 만들었습니다.

The second reason is recording translators and their contribution in clear way. Text files could be well tracked by Git so I chose it as a tracker. By using Git, we can get free lunch benefits from its toolchain and ecosystems like GitHub. We can track down the translation history only by reading Git commit history.
<br>두번째 이유는 번역자와 그들의 기여를 명확한 방법으로 기록하기 위해서입니다. 텍스트 파일은 Git으로 잘 관리할 수 있으므로 Git을 선택했습니다. Git을 쓰면 그것의 툴체인과 에코시스템을 공짜로 사용할 수도 있습니다. Git 커밋 기록만 읽어도 번역 이력을 따라갈 수 있습니다.

## To add an article / 문서를 추가하려면

If you're familiar with Git and GitHub, then create a pull request with a new article(e.g. `new_article.md`) and the translation file(e.g. `new_article.ko.md`) within `articles` directory. [Netlify](https://netlify.com) will build it automatically and generate intermediate site for verification. 
<br>Git과 GitHub에 익숙한 분이라면, 새로운 문서(예: `new_article.md`)와 번역 파일(예: `new_article.ko.md`)를 함께 `articles` 디렉토리에 안에 생성한 후 풀 리퀘스트로 작성해주시면 됩니다. [Netlify](https://netlify.com)가 자동으로 빌드해서 확인용 임시 사이트를 만들어줍니다.

Or, just leave a URL with some explanation why it should be translated on [GitHub Issue](https://github.com/zerobased-co/muchtrans/issues/9).
<br>아니면, URL과 함께 해당 문서가 번역되어야 하는 이유를 [GitHub Issue](https://github.com/zerobased-co/muchtrans/issues/9)에 남겨주세요.

## To build muchtrans / muchtrans를 빌드하려면

On your Python environments,
<br>당신의 파이썬 환경에서,

```shell
$ pip install -r requirements.txt
$ python build.py
$ cd _build
$ python -m http.server
```
And connect to `http://localhost:8000` in your favour web browser.
<br>그리고 좋아하는 웹 브라우저에서 `http://localhost:8000`으로 접속하시면 됩니다.

## License

Original articles may have their own license. Translated articles can be published under `MIT license` as same as muchtrans codes.
<br>원본 문서는 각자의 라이센스를 가지고 있을 수 있습니다. 번역된 문서는 muchtrans 코드와 마찬가지로 `MIT License`를 통해 전달됩니다.
