import os
from flask import Flask, render_template, send_from_directory, abort
import markdown
from markdown.extensions import tables, fenced_code
import pymdownx.arithmatex as arithmatex
from livereload import Server

app = Flask(__name__)

# ── Directorios del proyecto ──────────────────────────────────────────────────
FICHAS_DIR  = 'fichas'
IMAGES_DIR  = 'imagenes'

# ── Ruta principal: bitácora ──────────────────────────────────────────────────
@app.route('/')
def index():
    os.makedirs(FICHAS_DIR, exist_ok=True)

    files = sorted(f for f in os.listdir(FICHAS_DIR) if f.endswith('.md'))

    sections = []
    for filename in files:
        filepath = os.path.join(FICHAS_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            html = markdown.markdown(
                f.read(),
                extensions=[
                    'tables',
                    'fenced_code',
                    'pymdownx.arithmatex',
                ],
                extension_configs={
                    'pymdownx.arithmatex': {
                        'generic': True,
                    }
                }
            )
        sections.append(html)

    content_html = "<hr class='page-break'>".join(sections)
    return render_template('base.html', content=content_html)

# ── Ruta del diagrama animado ─────────────────────────────────────────────────
@app.route('/diagrama')
def diagrama():
    return render_template('diagrama.html')

# ── Servir imágenes estáticas desde /imagenes/ ────────────────────────────────
@app.route('/imagenes/<path:filename>')
def serve_image(filename):
    images_path = os.path.join(app.root_path, IMAGES_DIR)
    if not os.path.exists(os.path.join(images_path, filename)):
        abort(404)
    return send_from_directory(images_path, filename)

# ── Servidor con live-reload ──────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs(IMAGES_DIR, exist_ok=True)

    server = Server(app.wsgi_app)
    server.watch(f'{FICHAS_DIR}/*.md')
    server.watch('templates/*.html')
    server.watch(f'{IMAGES_DIR}/*')      # recarga si cambias imágenes
    server.serve(port=5000, debug=True)