from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import Tool, StructuredTool

def get_top_headlines() -> List[Dict[str, str]]:
    print("Getting top headlines")
    return [
        {"title": "Breaking News", "source": "CNN", "url": "https://example.com/1"},
        {"title": "Local Update", "source": "Local News", "url": "https://example.com/2"},
        {"title": "Technology News", "source": "Tech Daily", "url": "https://example.com/3"}
    ]

def get_news_by_category(category: str) -> List[Dict[str, str]]:
    print(f"Getting news by category: {category}")
    return [
        {"title": f"{category} News 1", "source": "News Source", "url": "https://example.com/4"},
        {"title": f"{category} News 2", "source": "News Source", "url": "https://example.com/5"}
    ]

def search_news(query: str) -> List[Dict[str, str]]:
    print(f"Searching news for: {query}")
    return [
        {"title": f"Result for {query} 1", "source": "News Source", "url": "https://example.com/6"},
        {"title": f"Result for {query} 2", "source": "News Source", "url": "https://example.com/7"}
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
