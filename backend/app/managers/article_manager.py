from app.models import db, Article as ArticleModel
from app.exceptions.errors import DBCommitError
from datetime import datetime, timedelta


class Article:
    def __init__(self, article_model: ArticleModel):
        self.id = article_model.id
        self.ticker = article_model.ticker
        self.title = article_model.title
        self.media = article_model.media
        self.published_date = article_model.published_date
        self.url = article_model.url
        self.clean_url = article_model.clean_url
        self.compressed_summary = article_model.compressed_summary
        self.sentiment = article_model.sentiment
        self.impact = article_model.impact

    def to_json(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "title": self.title,
            "media": self.media,
            "published_date": self.published_date,
            "url": self.url,
            "clean_url": self.clean_url,
            "compressed_summary": self.compressed_summary,
            "sentiment": self.sentiment,
            "impact": self.impact,
        }


class ArticleManager:

    @staticmethod
    def get_article_by_id(article_id: int):
        article = ArticleModel.query.get(article_id)
        return Article(article)

    @staticmethod
    def get_article_by_title_and_ticker(article_title: str, ticker: str):
        article = ArticleModel.query.filter_by(
            title=article_title, ticker=ticker
        ).one_or_none()
        if article is None:
            return None
        return Article(article)

    @staticmethod
    def get_articles_by_ticker(ticker: str, time_period: int, limit: int = 100):
        cutoff_date = datetime.now() - timedelta(days=time_period)
        article_queries = (
            ArticleModel.query.filter(
                ArticleModel.ticker == ticker,
                ArticleModel.published_date >= cutoff_date,
            )
            .order_by(ArticleModel.published_date.desc())
            .limit(limit)
            .all()
        )
        return [Article(article) for article in article_queries]

    @staticmethod
    def get_articles_by_ticker_paginated(
        ticker: str, time_period: int, page: int, limit: int
    ):
        cutoff_date = datetime.now() - timedelta(days=time_period)
        article_queries = (
            ArticleModel.query.filter(
                ArticleModel.ticker == ticker,
                # ArticleModel.published_date >= cutoff_date,
            )
            .order_by(ArticleModel.published_date.desc())
            .paginate(page=page, per_page=limit)
        )

        articles = [Article(article) for article in article_queries.items]
        return {"articles": articles, "has_more": article_queries.has_next}

    @staticmethod
    def add_article(
        ticker: str,
        title: str,
        compressed_summary: str,
        sentiment: str,
        impact: str,
        url: str = None,
        published_date: datetime = None,
        clean_url: str = None,
        media: str = None,
    ):
        new_article = ArticleModel(
            ticker=ticker,
            title=title,
            media=media,
            published_date=published_date,
            url=url,
            clean_url=clean_url,
            compressed_summary=compressed_summary,
            sentiment=sentiment,
            impact=impact,
        )
        try:
            db.session.add(new_article)
            db.session.commit()
            return new_article
        except Exception as e:
            db.session.rollback()
            raise DBCommitError(f"Error saving article: {e}")

    @staticmethod
    def delete_old_articles(days: int) -> int:
        threshold_date = datetime.now() - timedelta(days=days)
        try:
            deleted_count = db.session.query(ArticleModel).filter(
                ArticleModel.published_date < threshold_date
            ).delete(synchronize_session=False)

            db.session.commit()
            return deleted_count
        except Exception as e:
            db.session.rollback()
            raise DBCommitError(f"Error deleting articles: {e}")
