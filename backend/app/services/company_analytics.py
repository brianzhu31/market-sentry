from managers.article_manager import ArticleManager
from managers.company_manager import CompanyManager
from lib.inference.batch import create_jsonl_batch_file, submit_batch, get_batch_results
from lib.inference.prompt import sentiment_summary_prompt
from typing import List, Dict
import json


class SummaryCollection:

    def __init__(self, company_name: str, ticker: str, summaries: str):
        self.company_name = company_name
        self.ticker = ticker
        self.summaries = summaries


class CompanyAnalyticsEngine:

    def __init__(self, tickers: str = None):
        self.tickers: List[str] = tickers
        self.summary_collections: List[SummaryCollection] = []
        self.article_pool: Dict = {}

    @staticmethod
    def sentiment_to_int_score(sentiment: str):
        mapping = {
            "VERY NEGATIVE": 1,
            "NEGATIVE": 2,
            "NEUTRAL": 3,
            "POSITIVE": 4,
            "VERY POSITIVE": 5,
        }
        return mapping.get(sentiment, 3)

    @staticmethod
    def impact_to_int_score(impact: str):
        mapping = {"LOW": 1, "MEDIUM": 3, "HIGH": 5}
        return mapping.get(impact, 1)

    def format_summary_points(self, ticker: str, points: Dict):
        formatted_points = []
        for point in points:
            source = None
            article_index = int(point["source"])
            if (0 <= article_index < len(self.article_pool[ticker])):  
                article = self.article_pool[ticker][article_index]
                source = {
                    "title": article.title,
                    "url": article.url,
                    "clean_url": article.clean_url,
                    "published_date": article.published_date.strftime('%Y-%m-%d %H:%M:%S') if article.published_date else None
                }
            formatted_points.append({
                "info": point["info"],
                "source": source
            })
        return formatted_points


    def generate_overall_summaries(self, time_period: int):
        company_sentiment_scores = {}
        for ticker in self.tickers:
            company_query = CompanyManager.get_company_by_ticker(ticker=ticker)
            if not company_query:
                return
            company_name = company_query.company_name
            articles_for_ticker = ArticleManager.get_articles_by_ticker(
                ticker=ticker, time_period=time_period)
            self.article_pool[ticker] = articles_for_ticker

            total_score = 0
            total_weight = 0
            for article in articles_for_ticker:
                sentiment = article.sentiment
                impact = article.impact
                int_score = self.sentiment_to_int_score(sentiment)
                int_weight = self.impact_to_int_score(impact)
                total_score += int_score * int_weight
                total_weight += int_weight

            overall_score = total_score / total_weight if total_weight != 0 else 0
            company_sentiment_scores[ticker] = round(overall_score, 1)

            summaries_text_list = []
            for index, article in enumerate(articles_for_ticker):
                summaries_text_list.append(
                    f"Article_index: {index}\nArticle Title: {article.title}\nSummary:\n{article.compressed_summary}\n"
                )

            summaries_text = "\n\n".join(summaries_text_list)

            print(summaries_text)

            summary_collection = SummaryCollection(
                company_name=company_name, ticker=ticker, summaries=summaries_text)
            self.summary_collections.append(summary_collection)

        create_jsonl_batch_file(
            objects=self.summary_collections,
            output_dir="files",
            file_name="summary_collections.jsonl",
            prompt_function=sentiment_summary_prompt,
            prompt_args=["company_name", "summaries"],
            output_json=True,
            custom_id_key="ticker"
        )

        batch_id = submit_batch(
            filepath="files/summary_collections.jsonl",
            endpoint="/v1/chat/completions",
            job_description="companies analysis job",
        )

        analysis_batch_output = get_batch_results(
            batch_id=batch_id,
            output_dir="files",
            output_filename="companies_analysis.jsonl",
        )

        for company_analytics in analysis_batch_output:
            ticker = company_analytics["custom_id"]
            text_output = company_analytics["response"]["body"]["choices"][0]["message"]["content"]
            json_output = json.loads(text_output)
            overall_summary = json_output["overall_summary"]
            positive_points = self.format_summary_points(ticker=ticker, points=json_output["positive"])
            negative_points = self.format_summary_points(ticker=ticker, points=json_output["negative"])

            CompanyManager.add_analysis_data(
                ticker=ticker,
                overall_summary=overall_summary,
                positive_summaries=positive_points,
                negative_summaries=negative_points,
                score=company_sentiment_scores[ticker]
            )
