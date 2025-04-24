from agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import StructuredTool

def search_products(query: str) -> List[Dict[str, Any]]:
    print(f"Searching products for: {query}")
    return [
        {"name": f"{query} Product 1", "price": 19.99, "store": "Store A", "in_stock": True},
        {"name": f"{query} Product 2", "price": 29.99, "store": "Store B", "in_stock": True},
        {"name": f"{query} Product 3", "price": 39.99, "store": "Store C", "in_stock": False}
    ]

def get_shopping_history() -> List[Dict[str, Any]]:
    print("Getting shopping history")
    return [
        {"date": "2023-04-15", "items": ["Item 1", "Item 2"], "total": 49.98},
        {"date": "2023-04-10", "items": ["Item 3"], "total": 19.99},
        {"date": "2023-04-05", "items": ["Item 4", "Item 5", "Item 6"], "total": 89.97}
    ]

def get_current_offers() -> List[Dict[str, Any]]:
    print("Getting current offers")
    return [
        {"item": "Item 1", "discount": "20%", "valid_until": "2023-04-30"},
        {"item": "Item 2", "discount": "10%", "valid_until": "2023-05-15"},
        {"item": "Item 3", "discount": "15%", "valid_until": "2023-04-25"}
    ]

def add_to_cart(item: str, quantity: int = 1) -> Dict[str, Any]:
    print(f"Adding {quantity} of {item} to cart")
    return {"status": "added", "item": item, "quantity": quantity}

def checkout() -> Dict[str, Any]:
    print("Checking out cart")
    return {"status": "completed", "order_id": "12345", "total": 69.98}


class ShoppingAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Shopping Agent"
        self.slug = "shopping"
        self.description = "Responsible for shopping for groceries and other items from the shopping API."
        
        # Mock function tools for shopping operations
        self.tools = [
            StructuredTool.from_function(
                name="search_products",
                description="Search for products",
                func=search_products,
                args_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search term to find products"
                        }
                    },
                    "required": ["query"]
                }
            ),
            StructuredTool.from_function(
                name="get_shopping_history",
                description="Get shopping history",
                func=get_shopping_history,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_current_offers",
                description="Get current offers and discounts",
                func=get_current_offers,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="add_to_cart",
                description="Add an item to cart",
                func=add_to_cart,
                args_schema={
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "ID of the product to add to cart"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity of the product to add"
                        }
                    },
                    "required": ["product_id", "quantity"]
                }
            ),
            StructuredTool.from_function(
                name="checkout",
                description="Checkout the cart",
                func=checkout,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
