from dataclasses import dataclass


@dataclass
class Quote:
    content: str
    author: str
    tags: list[str]


@dataclass
class StoredQuote(Quote):
    _id: str


@dataclass
class AIAnalysis:
    quote: StoredQuote
    ai_analysis: str
