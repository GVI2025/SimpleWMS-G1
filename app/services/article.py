from sqlalchemy.orm import Session
from app.models import Article as ArticleModel, CategorieArticle
from app.schemas.article import ArticleCreate, ArticleUpdate

from typing import Optional

def get_article(db: Session, article_id: str):
    return db.query(ArticleModel).filter(ArticleModel.id == article_id).first()

def get_article_by_sku(db: Session, sku: str):
    return db.query(ArticleModel).filter(ArticleModel.sku == sku).first()

def list_articles(db: Session, skip: int = 0, limit: int = 100, categorie: Optional[CategorieArticle] = None):
    query = db.query(ArticleModel)
    if categorie is not None:
        query = query.filter(ArticleModel.categorie == categorie)
    return query.offset(skip).limit(limit).all()

def create_article(db: Session, article: ArticleCreate):
    db_article = ArticleModel(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: str, article_data: ArticleUpdate):
    db_article = get_article(db, article_id)
    if db_article:
        for key, value in article_data.dict().items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: str):
    db_article = get_article(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article
