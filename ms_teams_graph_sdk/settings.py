from typing import Optional, Text, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class.
    """

    # Microsoft Graph API settings
    MICROSOFT_GRAPH_BASE_API_URL: Text = "https://graph.microsoft.com/"
    MICROSOFT_GRAPH_API_VERSION: Text = "v1.0"
    PAGINATION_COUNT: Optional[int] = 20
    DEFAULT_SCOPES: List = [
    'https://graph.microsoft.com/User.Read',
    'https://graph.microsoft.com/Group.Read.All',
    'https://graph.microsoft.com/ChannelMessage.Send',
    'https://graph.microsoft.com/Chat.Read',
    'https://graph.microsoft.com/ChatMessage.Send',
]


settings = Settings()