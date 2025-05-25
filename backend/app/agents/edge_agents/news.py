from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import Tool, StructuredTool

from loguru import logger

def get_top_headlines() -> List[Dict[str, Any]]:
    logger.info("Getting top headlines")
    return [
        {"id": 1, "newspaper": "The Washington Post", "subject": "Trump, visiting Capitol Hill, warns House Republicans against opposing his bill", "preview": "President Donald Trump warned House Republicans against opposing his massive tax and immigration bill as he visited Capitol Hill on Monday in a bid to bolster support for the package.", "date": "May 20, 2025"},
        {"id": 2, "newspaper": "The New York Times", "subject": "New Orleans Jail Employee Is Arrested and Charged With Helping 10 Inmates Escape", "preview": "A maintenance worker shut off water at the jail, allowing the inmates to remove a toilet and sink fixture from a cell wall, according to the Louisiana attorney general's office.", "date": "May 20, 2025"},
        {"id": 3, "newspaper": "engadget", "subject": "Everything announced at the Google I/O 2025 keynote", "preview": "A tidal wave of AI updates (plus some other stuff).", "date": "May 20, 2025"}
    ]

def get_news_by_category(category: str) -> List[Dict[str, Any]]:
    logger.info(f"Getting news by category: {category}")
    return [
        {"id": 4, "newspaper": "News Source", "subject": f"{category} News 1", "preview": f"This is a preview of {category} news article 1", "date": "May 19, 2025"},
        {"id": 5, "newspaper": "News Source", "subject": f"{category} News 2", "preview": f"This is a preview of {category} news article 2", "date": "May 19, 2025"}
    ]

def search_news(query: str) -> List[Dict[str, Any]]:
    logger.info(f"Searching news for: {query}")
    return [
        {"id": 6, "newspaper": "News Source", "subject": f"Result for {query} 1", "preview": f"This is a preview of search result for {query} 1", "date": "May 18, 2025"},
        {"id": 7, "newspaper": "News Source", "subject": f"Result for {query} 2", "preview": f"This is a preview of search result for {query} 2", "date": "May 18, 2025"}
    ]


class NewsAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "News Agent"
        self.slug = "news"
        self.description = "Responsible for getting the news information from the news API."
        
        # Mock function tools for news operations
        self.tools = [
            StructuredTool.from_function(
                name="get_top_headlines",
                description="Get the top news headlines",
                func=get_top_headlines,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_news_by_category",
                description="Get news by category",
                func=get_news_by_category,
                args_schema={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Category of news to get (e.g., technology, sports, politics)"
                        }
                    },
                    "required": ["category"]
                }
            ),
            StructuredTool.from_function(
                name="search_news",
                description="Search for news articles",
                func=search_news,
                args_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search term to find news articles"
                        }
                    },
                    "required": ["query"]
                }
            )
        ]
