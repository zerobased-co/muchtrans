from collections import defaultdict
from datetime import datetime
from git import Repo
from jinja2 import Environment, FileSystemLoader
from mistune_contrib.meta import parse as md_parse
import glob
import mistune
import os
import pytz
import re
import requests
import time

OUTPUT = '_build'

SINGLE = ['blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', ]
SINGLE_RE = '^({})'.format('|'.join(['\<{} '.format(_) for _ in SINGLE]))

SPLITTER = ['p', 'ol', 'ul', 'div', 'img', 'object']
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
        prefix = self.options.get('heading_prefix', '')

        html = '<h{} id="{}{}">{}</h{}>\n'.format(
            level, prefix, self.id_count, text, level
        )
        return html 


class CustomImageMixin(object):
    """
    Mixin for 
        - Rendering embed tag for SVG images
        - Adding a custom class '.image' for images
    """
    def image(self, src, title, text):
        html = super().image(src, title, text)
        
        # Add custom class
        html = html.replace('<img', '<img class="image"')

        # Change tag for SVG
        if src.lower()[-4:] == '.svg':
            html = html.replace('<img', '<embed')

        return html


class MuchtransRenderer(HLabelMixin, CustomImageMixin, mistune.Renderer):
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


def get_authors_from_commits(commits):
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


def get_commits(repo, filepath):
    commits = list(repo.iter_commits('--all', paths=filepath))
    return commits


def get_time_from_commit(commit):
    return datetime.fromtimestamp(commit.authored_date + commit.author_tz_offset).replace(tzinfo=pytz.utc)

def get_UTC(datetime):
    return datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

def get_RFC822(datetime):
    return datetime.strftime("%a, %d %b %Y %H:%M:%S +0000")

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
translated_articles_by_language = defaultdict(list)
translated_articles_in_month = defaultdict(list)

for key, article in articles.items():
    with open(article['original']) as file:
        original = file.read()

    original_metadata, original = md_parse(original)
    article['metadata'] = original_metadata
    original_html = mistune.Markdown(renderer=MuchtransRenderer(escape=False, hard_wrap=True))(original).replace('<br>', '</p><p>')
    print('Building: {}'.format(article['metadata'].get('title', key)))

    # Find dedicated css file
    css_filename = '/static/articles/{}/style.css'.format(os.path.splitext(os.path.basename(article['original']))[0])
    if os.path.isfile(OUTPUT + css_filename):
        css = css_filename
    else:
        css = None

    for language, filename in article['translations'].items():
        with open(filename) as file:
            translation = file.read()

        translation_metadata, translation = md_parse(translation)
        translation_html_filename = '/translations/' + os.path.splitext(os.path.basename(filename))[0] + '.html'
        translation_html = mistune.Markdown(renderer=MuchtransRenderer(escape=False, hard_wrap=True, heading_prefix='t_'))(translation).replace('<br>', '</p><p>')

        # TBD: Fix for duplicated footnote (will be fixed in renderer level, future)
        translation_html = translation_html.replace('fn-', 'tfn-').replace('fnref-', 'tfnref-')

        # Match original and translated articles in html level
        rows = []
        sbuf = dbuf = ''

        # Mark for untranslated
        untranslated = False

        for s, d in zip(original_html.split('\n'), translation_html.split('\n')):
#            if len(s) > 40 and s == d:  # TBD: Too naive approache
#                untranslated = True

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
                sbuf += s + '\n'
                dbuf += d + '\n'

        if sbuf:
            rows.append((sbuf, dbuf))

        # Render and save translated article
        context = {
            'css': css,
            'rows': rows,

            'filename': filename,
            'original': original_metadata,
            'translation': translation_metadata,

            'finished': not untranslated,
            'utterances': os.environ.get('PRODUCTION', False),
        }

        # Get commits from the repository
        commits = get_commits(repo, filename)

        if commits:
            # Add translation info into context
            context['translators'] = get_authors_from_commits(commits)
            context['latest_update'] = get_UTC(get_time_from_commit(commits[0]))

            # Add to the index
            created_month = get_time_from_commit(commits[-1]).strftime('%Y-%m')
            translated_articles_in_month[created_month].insert(0, {
                'title': article['metadata']['title'],
                'url': translation_html_filename,
            })

            # Prepare list for feed publishing
            translated_articles_by_language[language].append({
                'datetime': get_UTC(get_time_from_commit(commits[-1])),
                'pubDate': get_RFC822(get_time_from_commit(commits[-1])),
                'translators':  context['translators'],
                'title': article['metadata']['title'],
                'url': translation_html_filename,
                'description': translation_html,
            })

        # Let's render the final file
        rendered = article_template.render(context)

        with open(OUTPUT + translation_html_filename, "w") as file:
            file.write(rendered)

# RSS Feed
print('Building RSS feeds')
rss_template = env.get_template('templates/feed.xml')
feed_list = []
for language, articles in translated_articles_by_language.items():
    article_list = sorted(
        articles,
        key=lambda x: x['datetime'],
        reverse=True
    )[:10]
    rendered = rss_template.render({
        'hostname': 'https://muchtrans.com', # TODO: Should be loaded from ENV
        'pubDate': get_RFC822(datetime.utcnow()),
        'language': language,
        'articles': article_list,
    })

    print('\t RSS feed in {}'.format(language))
    filename = '/feeds/{}.xml'.format(language)
    with open(OUTPUT + filename, "w") as file:
        file.write(rendered)

    feed_list.append((language, filename))

# Render and save index
index_template = env.get_template('templates/index.html')
article_list = sorted(
    translated_articles_in_month.items(),
    key=lambda x: x[0],
    reverse=True
)
rendered = index_template.render({
    'article_list': article_list,
    'feed_list': feed_list,
})

with open(OUTPUT + '/index.html', "w") as file:
    file.write(rendered)
