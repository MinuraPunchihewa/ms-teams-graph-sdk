from typing import List, Optional, Text
from ms_teams_graph_sdk.auth import MSGraphAPIAuthManager
from ms_teams_graph_sdk.resources import ChannelsResource
from ms_teams_graph_sdk.client.ms_graph_api_base_client import MSGraphAPIBaseClient


class MSTeamsGraphAPIClient(MSGraphAPIBaseClient):
    def __init__(self, client_id: Text, client_secret: Text, tenant_id: Text, scopes: Optional[List] = None) -> None:
        # get access token from auth manager
        auth_manager = MSGraphAPIAuthManager(client_id, client_secret, tenant_id, scopes)
        access_token = auth_manager.get_access_token()
        # initialize the base client
        super().__init__(access_token)

        # initialize resources
        self.channels = ChannelsResource(self)
        