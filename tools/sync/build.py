"""Rebuild the site's index.html from the Claude Artifact "Jihyun Kim Portfolio".

The Artifact is the source of truth. This turns its page file into a single self-contained
index.html (CSS, JS and vendor libraries inline) with the Artifact-only owner editor removed.

  python3 -I tools/sync/build.py ARTIFACT_HTML REPO_ROOT --list-assets
      prints the Artifact asset ids (work images) that are not yet in REPO_ROOT/images/
  python3 -I tools/sync/build.py ARTIFACT_HTML REPO_ROOT [--version V --sha256 H]
      writes REPO_ROOT/index.html (and tools/sync/state.json when --version/--sha256 are given)
"""
import json, pathlib, re, sys, urllib.parse
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
args = sys.argv[1:]
flag = lambda name: args[args.index(name) + 1] if name in args else None
SRC, ROOT = pathlib.Path(args[0]), pathlib.Path(args[1])
src = SRC.read_text('utf-8')
if '<body>' in src:  # full page as the Artifact service saves it: keep only what the page itself wrote
    src = src[src.index('<body>') + 6:src.rindex('</body>')]


def between(s, a, b):
    i = s.index(a) + len(a)
    return s[i:s.index(b, i)]


css = between(src, '<style id="css">', '</style>')
tpl = between(src, '<template id="tpl">', '</template>')
works = json.loads(between(src, '<script type="application/json" id="works-data">', '</script>'))
app = between(src, '<script id="app">', '</script>')
fonts = between(src, '<link rel="stylesheet" href="https://fonts.googleapis.com', '">')

# ---------- work images: Artifact asset ids become files in images/ ----------
images = ROOT / 'images'
missing = []
for it in works.get('items', []):
    img = it.get('image') or ''
    if re.fullmatch(r'[0-9a-f]{32}', img):
        found = sorted(p for p in images.glob(img + '.*')) if images.is_dir() else []
        if found:
            it['image'] = 'images/' + found[0].name
        else:
            missing.append(img)
if '--list-assets' in args:
    print('\n'.join(missing))
    sys.exit(0)
if missing:
    sys.exit('missing work images, fetch these asset ids into images/ first: ' + ' '.join(missing))

# ---------- CSS: the reset the Artifact viewer supplies, then the page styles without the owner editor ----------
reset = ('/* base reset (previously supplied by the Artifact viewer) */\n'
         ':root { box-sizing: border-box; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }\n'
         'html { scroll-padding-top: env(safe-area-inset-top, 0px); }\n'
         'body { margin: 0; padding: 0; }\n'
         'img { max-width: 100%; }\n\n')
a = css.index('/* editor (owner only) */'); b = css.index('.ed-status {'); b = css.index('\n', b) + 1
css = css[:a] + css[b:]
css = css.replace('.editor:not([hidden]) { animation: edIn .8s var(--ease); }\n@keyframes edIn { from { transform: translateX(48px); opacity: 0; } }\n', '')
css = css.replace(' .editor:not([hidden]) { animation: none; }', '')
css = css.replace('the Works archive by discipline (owner-editable)', 'the Works archive by discipline')
assert not re.search(r'\.(editor|ed-[a-z]|edit-fab)', css), 'editor css left'
css = reset + css.strip() + '\n'

# ---------- markup: drop the owner-only editor ----------
tpl = re.sub(r'\n<button class="edit-fab".*?</aside>\n', '\n', tpl, flags=re.S)
assert 'editor' not in tpl and 'editFab' not in tpl, 'editor markup left'
tpl = tpl.replace('hidden=""', 'hidden').replace('data-fade=""', 'data-fade').replace('data-lines=""', 'data-lines')

# ---------- JS: static-site version ----------
s = app
a = s.index("  /* ── the page's own source, kept pristine"); b = s.index('  /* ── works data ── */')
s = s[:a] + s[b:]
a = s.index('  /* ── owner editing: republishes this page with the new works ── */'); b = s.index('  /* ── sound:')
s = s[:a] + s[b:]
# images: a path inside the project (images/...) or a full https URL instead of the Artifact asset store
s = s.replace("image: /^[0-9a-f]{32}$/.test(i.image || '') ? i.image : '' })) });",
              "image: /^(images\\/[\\w\\-./ ]+|https?:\\/\\/\\S+)$/i.test(i.image || '') ? String(i.image) : '' })) });")
s = s.replace("img.src = '/_blob/' + item.image;", "img.src = item.image;")
s = s.replace("pvImg.src = '/_blob/' + it.image;", "pvImg.src = it.image;")
assert '_blob' not in s and 'claude.use' not in s and 'buildDocument' not in s and 'tplEl' not in s, 'artifact-only code left'
js = '/* Jihyun Kim Portfolio — site script (GSAP, ScrollTrigger and Lenis are loaded before this one) */\n' + s.strip('\n')


def inline_js(code):
    code = code.rstrip()
    assert '</script' not in code.lower() and '<!--' not in code, 'script cannot be inlined'
    return '<script>\n' + code + '\n</script>'


vendor = '\n'.join(inline_js((HERE / 'vendor' / f).read_text('utf-8')) for f in ('gsap.min.js', 'ScrollTrigger.min.js', 'lenis.min.js'))
fav = 'data:image/svg+xml,' + urllib.parse.quote((HERE / 'favicon.svg').read_text('utf-8').strip(), safe=':/= ')
works_json = json.dumps(works, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Jihyun Kim Portfolio</title>
<meta name="description" content="Jihyun Kim — Entrepreneur. Creator. Artist. Everything I want, wants me more.">
<meta name="theme-color" content="#0a0708">
<meta property="og:type" content="website">
<meta property="og:title" content="Jihyun Kim Portfolio">
<meta property="og:description" content="Entrepreneur. Creator. Artist.">
<link rel="icon" href="{fav}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com{fonts}">
<style>
{css}
</style>
</head>
<body>
{tpl.strip()}

<!-- Works archive: edit this list to add or change works (see README.md) -->
<script type="application/json" id="works-data">{works_json}</script>
{vendor}
{inline_js(js)}
</body>
</html>
'''
(ROOT / 'index.html').write_text(html, 'utf-8')
print('index.html', len(html.encode()), 'bytes,', len(works.get('items', [])), 'works')

if flag('--version') and flag('--sha256'):
    state = {'artifact': 'https://claude.ai/artifact/UTC3V9MdeeLvjtouDpZCGn', 'version': flag('--version'),
             'sha256': flag('--sha256'), 'synced_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    (HERE / 'state.json').write_text(json.dumps(state, indent=2) + '\n', 'utf-8')
