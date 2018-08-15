from jinja2 import Template
import mistune
import os
import re

SPLITTER = ['blockquote', 'h1', 'h2', 'h3']
SPLITTER_RE = '^({})'.format('|'.join(['<{}>'.format(_) for _ in SPLITTER]))

with open('template.html') as file:
    template = Template(file.read())

articles = [
    {
        'title': 'Ryuichi Sakamoto – “We are destroying the world.”',
        'source_url': 'https://www.52-insights.com/ryuichi-sakamoto-we-are-destroying-the-world-interview-music/',
        'original': 'ryuichi-sakamoto-52-insights.md',
        'translations': {
            'ko': 'ryuichi-sakamoto-52-insights.ko.md',
        },
    },
]

for article in articles:
    with open(article['original']) as file:
        original = file.read()

    original_html_filename = os.path.splitext(article['original'])[0] + '.html'
    original_html = mistune.markdown(original)

    print('Building {}'.format(article['title']))

    for locale, filename in article['translations'].items():
        with open(filename) as file:
            translation = file.read()

        translation_html_filename = os.path.splitext(filename)[0] + '.html'
        translation_html = mistune.markdown(translation)

        print('\t{}: {}'.format(locale, original_html.count('\n')))

        rows = []
        sbuf = dbuf = ''
        for s, d in zip(original_html.split('\n'), translation_html.split('\n')):
            if re.search(SPLITTER_RE, s):
                if sbuf:
                    rows.append((sbuf, dbuf))
                rows.append((s, d))
                sbuf = dbuf = ''
            else:
                sbuf += s
                dbuf += d
        if sbuf:
            rows.append((sbuf, dbuf))
                

        rendered = template.render({
            'source_url': article['source_url'],
            'rows': rows,
        })

        with open(translation_html_filename, "w") as file:
            file.write(rendered)

