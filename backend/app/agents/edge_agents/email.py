from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import Tool, StructuredTool

from loguru import logger

def get_unread_emails() -> List[Dict[str, Any]]:
    logger.info("Getting unread emails")
    return [
        {"id": 1, "sender": "Google Haritalar", "subject": "Yorumlarınız Google Haritalar'da çok popüler.", "preview": "Yarattığınız etkiyi kutlayalım.", "date": "May 20", "read": False},
        {"id": 2, "sender": "LinkedIn", "subject": "New jobs similar to Software Engineer at LinkedIn", "preview": "Jobs similar to Software Engineer at LinkedIn", "date": "May 19", "read": True},
        {"id": 3, "sender": "The Postman Team", "subject": "New sign-in notification", "preview": "Review new sign-in activity We recently detected a new sign-in for your Postman account. If this was you, no further action is needed.", "date": "May 15", "read": True}
    ]

def search_emails(query: str) -> List[Dict[str, Any]]:
    logger.info(f"Searching emails for: {query}")
    return [
        {"id": "3", "from": "sender3@example.com", "subject": f"Email about {query}", "date": "2023-04-18"},
        {"id": "4", "from": "sender4@example.com", "subject": f"Regarding {query}", "date": "2023-04-17"}
    ]

def send_email(to: str, subject: str, body: str) -> Dict[str, Any]:
    logger.info(f"Sending email to {to} with subject: {subject}")
    return {"status": "sent", "to": to, "subject": subject}

def mark_email_as_read(email_id: str) -> Dict[str, Any]:
    logger.info(f"Marking email {email_id} as read")
    return {"status": "marked as read", "email_id": email_id}


class EmailAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Email Agent"
        self.slug = "email"
        self.description = "Responsible for getting the email information from the email IoT device."
        
        # Mock function tools for email operations
        self.tools = [
            StructuredTool.from_function(
                name="get_unread_emails",
                description="Get unread emails",
                func=get_unread_emails,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="search_emails",
                description="Search for emails",
                func=search_emails,
                args_schema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search term to find emails"
                        }
                    },
                    "required": ["query"]
                }
            ),
            StructuredTool.from_function(
                name="send_email",
                description="Send an email",
                func=send_email,
                args_schema={
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body content"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            ),
            StructuredTool.from_function(
                name="mark_email_as_read",
                description="Mark an email as read",
                func=mark_email_as_read,
                args_schema={
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "ID of the email to mark as read"
                        }
                    },
                    "required": ["email_id"]
                }
            )
        ]
