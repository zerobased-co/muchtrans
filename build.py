from jinja2 import Template
import mistune
import os
import re


SINGLE = ['blockquote', 'h1', 'h2', 'h3', 'hr', ]
SINGLE_RE = '^({})'.format('|'.join(['\<{}>'.format(_) for _ in SINGLE]))

SPLITTER = ['ol', 'ul', 'div', ]
SPLITTER_RE = '^({})'.format('|'.join(['\<{}'.format(_) for _ in SPLITTER]))

IGNORE = ['div', ]
IGNORE_RE = '^({})'.format('|'.join(['\<{} |\</{}>'.format(_, _) for _ in IGNORE]))

articles = [
    {
        'title': 'Becoming a 10x Developer',
        'source_url': 'https://kateheddleston.com/blog/becoming-a-10x-developer',
        'original': '10xdeveloper.md',
        'translations': {
            'ko': '10xdeveloper.ko.md',
        },
    },
    {
        'title': 'Tim Cook\'s memo at AAPL hits $1 trillion market cap',
        'source': 'Tim Cook thanks employees in memo following record-setting $1 trillion market cap',
        'source_url': 'https://9to5mac.com/2018/08/02/apple-tim-cook-email-1-trillion/',
        'original': 'timcook-letter-1t.md',
        'translations': {
            'ko': 'timcook-letter-1t.ko.md',
        },
    },
    {
        'title': 'Ryuichi Sakamoto – “We are destroying the world.”',
        'source_url': 'https://www.52-insights.com/ryuichi-sakamoto-we-are-destroying-the-world-interview-music/',
        'original': 'ryuichi-sakamoto-52-insights.md',
        'translations': {
            'ko': 'ryuichi-sakamoto-52-insights.ko.md',
        },
    },
    {
        'title': 'Python Community Interview With Mariatta Wijaya',
        'source_url': 'https://realpython.com/interview-mariatta-wijaya/',
        'original': 'interview-mariatta-wijaya.md',
        'translations': {
            'ko': 'interview-mariatta-wijaya.ko.md',
        },
    },
]


# Create articles
translated_articles = []

with open('templates/article.html') as file:
    article_template = Template(file.read())

for article in articles:
    with open('articles/' + article['original']) as file:
        original = file.read()

    original_html = mistune.markdown(original, escape=False, hard_wrap=True).replace('<br>', '</p><p>')
    print('Building: {}'.format(article['title']))

    for locale, filename in article['translations'].items():
        with open('articles/' + filename) as file:
            translation = file.read()

        translation_html_filename = os.path.splitext(filename)[0] + '.html'
        translation_html = mistune.markdown(translation, escape=False, hard_wrap=True).replace('<br>', '</p><p>')

        rows = []
        sbuf = dbuf = ''

        for s, d in zip(original_html.split('\n'), translation_html.split('\n')):
            if re.search(SINGLE_RE, s):
                if sbuf:
                    rows.append((sbuf, dbuf))
                    sbuf = dbuf = ''
                rows.append((s, d))
            elif re.search(IGNORE_RE, s):
                continue
            else:
                if re.search(SPLITTER_RE, s):
                    if sbuf:
                        rows.append((sbuf, dbuf))
                        sbuf = dbuf = ''
                sbuf += s
                dbuf += d

        if sbuf:
            rows.append((sbuf, dbuf))

        rendered = article_template.render({
            'article': article,
            'rows': rows,
        })

        with open(translation_html_filename, "w") as file:
            file.write(rendered)

        translated_articles.append({
            'title': article['title'],
            'url': translation_html_filename,
        })

# Create index
with open('templates/index.html') as file:
    index_template = Template(file.read())

rendered = index_template.render({
    'articles': translated_articles,
})

with open('index.html', "w") as file:
    file.write(rendered)
