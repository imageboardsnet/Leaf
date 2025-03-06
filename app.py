from flask import Flask,send_from_directory
from flask_sitemapper import Sitemapper
import os
import ibrender
from markupsafe import Markup

def create_app():
    app = Flask(__name__)
    
    # Configure static folder for articles
    app.static_folder = 'static'
    articles_static = os.path.join(os.path.dirname(__file__), 'articles')
    app.config['ARTICLES_FOLDER'] = articles_static
    
    # Initialize extensions
    sitemapper = Sitemapper()
    sitemapper.init_app(app)
    ibrender.init_app(app)  # Initialize ibrender with our app instance
    
    # Register filters
    @app.template_filter('nl2br')
    def nl2br(value):
        if not value:
            return ''
        return Markup(value.replace('\n', '<br>\n'))
    
    # Register routes
    @app.route('/')
    def home():
        return ibrender.render_blog()

    @app.route('/blog/category/<category>')
    def blog_category(category):
        return ibrender.render_blog(category)

    @app.route('/blog/<path:article_id>')
    def article(article_id):
        return ibrender.render_article(article_id)

    @app.route('/static/articles/<path:filename>')
    def article_static(filename):
        return send_from_directory(app.config['ARTICLES_FOLDER'], filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/robots.txt')
    def robots():
        return send_from_directory(os.path.join(app.root_path, 'static'),'robots.txt', mimetype='text/plain')

    @app.route("/sitemap.xml")
    def sitemap():
        return sitemapper.generate()

    @app.errorhandler(404)
    def page_not_found(e):
        return ibrender.render_404()
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run() 
