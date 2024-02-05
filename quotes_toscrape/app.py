import random
from fastapi import FastAPI, Query, BackgroundTasks
from quotes_toscrape.ai_completion import get_maritalk_analysis
from quotes_toscrape.entities import StoredQuote, AIAnalysis
from quotes_toscrape.quotes_scraper import scrape_all_quotes
from quotes_toscrape.database import QuotesRepository

app = FastAPI(title="Quotes API")


def scrape_and_store_quotes_background():
    all_quotes = scrape_all_quotes()
    QuotesRepository.insert_many(all_quotes)


@app.post("/scrape")
def scrape_and_store_quotes(bg: BackgroundTasks):
    bg.add_task(scrape_and_store_quotes_background)
    return {
        "message": "Quotes being scraped and stored in the background."
    }


@app.get("/", response_model=list[StoredQuote])
def get_all_quotes():
    return QuotesRepository.find_all()


@app.get("/search", response_model=list[StoredQuote])
def search_quotes(search_term: str = Query(max_length=100)):
    return QuotesRepository.find_all(
        {"content": {"$regex": search_term, "$options": "i"}}
    )


@app.get("/random_analysis")
def random_quote_analysis():
    all_quotes = QuotesRepository.find_all()
    random_quote = random.choice(all_quotes)
    ai_analysis = get_maritalk_analysis(random_quote)
    return AIAnalysis(
        quote=random_quote,
        ai_analysis=ai_analysis,
    )
