import os
import re
from typing import Dict, List, Optional, Set

class Article:
    def __init__(self, id: str, date: str, title: str, description: str, content: str, categories: List[str]):
        self.id = id
        self.date = date
        self.title = title
        self.description = description
        self.content = content
        self.categories = categories
        # Check if article.webp exists in the same directory as the article
        article_dir = os.path.join(os.path.dirname(__file__), 'articles', os.path.dirname(id))
        image_path = os.path.join(article_dir, 'article.webp')
        self.has_image = os.path.exists(image_path)
        self.image_url = f'/static/articles/{os.path.dirname(id)}/article.webp' if self.has_image else None

def parse_article_file(file_path: str, article_id: str) -> Optional[Article]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract metadata using regex
        date_match = re.search(r'\[date:(.*?)\]', content)
        title_match = re.search(r'\[title:(.*?)\]', content)
        desc_match = re.search(r'\[description:(.*?)\]', content)
        categories_match = re.search(r'\[categories:(.*?)\]', content)
        
        if not all([date_match, title_match, desc_match]):
            return None
            
        # Parse categories (default to ['Uncategorized'] if not specified)
        categories = []
        if categories_match:
            # Strip whitespace from the entire categories string and each individual category
            categories = [cat.strip() for cat in categories_match.group(1).strip().split(',')]
        if not categories:
            categories = ['Uncategorized']
            
        # Remove metadata from content
        main_content = re.sub(r'\[(?:date|title|description|categories):.*?\]\n?', '', content).strip()
        
        return Article(
            id=article_id,
            date=date_match.group(1).strip(),
            title=title_match.group(1).strip(),
            description=desc_match.group(1).strip(),
            content=main_content,
            categories=categories
        )
    except Exception as e:
        print(f"Error parsing article {file_path}: {str(e)}")
        return None

def get_all_articles() -> List[Article]:
    articles = []
    articles_dir = os.path.join(os.path.dirname(__file__), 'articles')
    
    # Walk through all subdirectories in the articles folder
    for root, dirs, files in os.walk(articles_dir):
        for file in files:
            if file.endswith('.txt'):
                # Use the directory name + file name (without extension) as the article ID
                relative_path = os.path.relpath(root, articles_dir)
                article_id = os.path.join(relative_path, os.path.splitext(file)[0])
                
                full_path = os.path.join(root, file)
                article = parse_article_file(full_path, article_id)
                if article:
                    articles.append(article)
    
    # Sort articles by date (newest first)
    return sorted(articles, key=lambda x: x.date, reverse=True)

def get_article_by_id(article_id: str) -> Optional[Article]:
    articles_dir = os.path.join(os.path.dirname(__file__), 'articles')
    article_path = os.path.join(articles_dir, f"{article_id}.txt")
    
    if os.path.exists(article_path):
        return parse_article_file(article_path, article_id)
    return None

def get_all_categories() -> Set[str]:
    """Get a list of all unique categories across all articles."""
    categories = set()
    for article in get_all_articles():
        categories.update(article.categories)
    return sorted(categories)

def get_articles_by_category(category: str) -> List[Article]:
    """Get all articles that belong to a specific category."""
    return [
        article for article in get_all_articles()
        if category in article.categories
    ]
