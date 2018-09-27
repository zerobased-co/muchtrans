from collections import defaultdict
from git import Repo
from jinja2 import Environment, FileSystemLoader
from mistune_contrib.meta import parse as md_parse
import glob
import mistune
import os
import re
import requests
import time


SINGLE = ['blockquote', 'h1', 'h2', 'h3', 'hr', ]
SINGLE_RE = '^({})'.format('|'.join(['\<{} '.format(_) for _ in SINGLE]))

SPLITTER = ['p', 'ol', 'ul', 'div', ]
SPLITTER_RE = '^({})'.format('|'.join(['\<{}'.format(_) for _ in SPLITTER]))

IGNORE = ['div', ]
IGNORE_RE = '^({})'.format('|'.join(['\<{} |\</{}>'.format(_, _) for _ in IGNORE]))

repo = Repo('.')

env = Environment(loader=FileSystemLoader('.'))

class HLabelMixin(object):
    """
    Mixin for adding id for each heading tag
    """
    id_count = 0

    def header(self, text, level, raw=None):
        self.id_count += 1
        rv = '<h%d id="%d">%s</h%d>\n' % (
            level, self.id_count, text, level
        )
        return rv

class HLabelRenderer(HLabelMixin, mistune.Renderer):
    pass


_github_users = {}
def get_github_user(email):
    if not os.environ.get('PRODUCTION', False):
        return {}

    if email in _github_users:
        return _github_users[email]

    headers = {
        'Authorization': 'token {}'.format(os.environ['GITHUB_ACCESS_TOKEN']),
    }
    r = requests.get('https://api.github.com/search/users?q={}+in:email'.format(email), headers=headers).json()

    try:
        if r['total_count'] >= 1:
            _github_users[email] = r['items'][0]
            return r['items'][0]
    except KeyError:
        pass

    return None


def get_authors(repo, filepath):
    commits = repo.iter_commits('--all', paths=filepath)

    authors = {}
    for commit in commits:
        email = commit.author.email

        if authors.get(email):
            authors[email]['count'] += 1
        else:
            authors[email] = {
                'name': commit.author.name,
                'email': email,
                'github': get_github_user(email),
                'count': 1,
            }

    return sorted(authors.values(), key=lambda x: x['count'], reverse=True)


def get_latest_updated(repo, filepath):
    commit = list(repo.iter_commits('--all', paths=filepath, max_count=1))

    if commit:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(commit[0].authored_date))

    return ''


# Get articles
articles = defaultdict(lambda: {
    'original': None,
    'translations': {},
})
for filename in glob.glob("articles/*.md"):
    # Original articles do not have any locale/language information in filename
    ORIGINAL_RE = '^([^\.]+)\.md$'
    TRANSLATION_RE = '^([^\.]+)\.([^\.]+)\.md$'
    key = os.path.basename(filename).split('.')[0]

    if re.search(ORIGINAL_RE, filename):
        articles[key]['original'] = filename
    else:
        result = re.search(TRANSLATION_RE, filename)
        if result:
            articles[key]['translations'][result[2]] = filename

# Prepare a template for articles
article_template = env.get_template('templates/article.html')

# Create translated articles
translated_articles = []
for key, article in articles.items():
    with open(article['original']) as file:
        original = file.read()

    original_metadata, original = md_parse(original)
    article['metadata'] = original_metadata
    original_html = mistune.Markdown(renderer=HLabelRenderer(escape=False, hard_wrap=True))(original).replace('<br>', '</p><p>')
    print('Building: {}'.format(article['metadata'].get('title', key)))

    # Find dedicated css file
    css_filename = 'static/css/{}.css'.format(os.path.splitext(os.path.basename(article['original']))[0])
    if os.path.isfile(css_filename):
        css = css_filename
    else:
        css = None

    for locale, filename in article['translations'].items():
        with open(filename) as file:
            translation = file.read()

        translation_metadata, translation = md_parse(translation)
        translation_html_filename = 'translations/' + os.path.splitext(os.path.basename(filename))[0] + '.html'
        translation_html = mistune.Markdown(renderer=HLabelRenderer(escape=False, hard_wrap=True))(translation).replace('<br>', '</p><p>')

        # Fix for duplicated footnote (will be fixed in renderer level, future)
        translation_html = translation_html.replace('fn-', 'tfn-').replace('fnref-', 'tfnref-')

        # Match original and translated articles in html level
        rows = []
        sbuf = dbuf = ''

        # Mark for untranslated
        untranslated = False

        for s, d in zip(original_html.split('\n'), translation_html.split('\n')):
            if len(s) > 40 and s == d:  # TBD: Too naive approache
                untranslated = True

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

        # Render and save translated article
        rendered = article_template.render({
            'css': css,
            'rows': rows,

            'translators': get_authors(repo, filename),
            'latest_update': get_latest_updated(repo, filename),

            'filename': filename,
            'original': original_metadata,
            'translation': translation_metadata,

            'finished': not untranslated,
        })

        with open(translation_html_filename, "w") as file:
            file.write(rendered)

        # Add to the index
        translated_articles.append({
            'title': article['metadata']['title'],
            'url': translation_html_filename,
        })

# Render and save index
index_template = env.get_template('templates/index.html')

rendered = index_template.render({
    'articles': translated_articles,
})

with open('index.html', "w") as file:
    file.write(rendered)
