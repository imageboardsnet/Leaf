from flask import render_template
from ibstrings import nothing_title, nothing_description, blog_title, blog_description
import ibutils

_app = None

def init_app(app):
    global _app
    _app = app

def render_404():
    with _app.app_context():
        all_categories = ibutils.get_all_categories()
        notfound_render = render_template('404.html')
        return render_template('index.html', 
                             content=notfound_render, 
                             title=nothing_title, 
                             description=nothing_description,
                             categories=all_categories)

def render_blog(category: str = None):
    with _app.app_context():
        all_categories = ibutils.get_all_categories()
        
        if category:
            articles = ibutils.get_articles_by_category(category)
            title = f"{blog_title} - {category}"
            description = f"Articles in category: {category}"
        else:
            articles = ibutils.get_all_articles()
            title = blog_title
            description = blog_description
            
        blog_render = render_template('blog.html', 
                                    articles=articles,
                                    categories=all_categories,
                                    current_category=category)
        return render_template('index.html', 
                             content=blog_render, 
                             title=title, 
                             description=description,
                             categories=all_categories,
                             current_category=category)

def render_article(article_id: str):
    with _app.app_context():
        article = ibutils.get_article_by_id(article_id)
        if not article:
            return render_404()
        
        all_categories = ibutils.get_all_categories()
        article_render = render_template('article.html', article=article)
        return render_template('index.html', 
                             content=article_render, 
                             title=article.title, 
                             description=article.description,
                             categories=all_categories)