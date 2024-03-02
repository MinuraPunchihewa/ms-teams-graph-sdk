import msal
import json
from typing import Text, Optional, List
from ms_teams_graph_sdk.settings import settings
from ms_teams_graph_sdk.utilities import get_logger
from ms_teams_graph_sdk.exceptions import AuthException
from ms_teams_graph_sdk.client.ms_graph_api_base_client import MSGraphAPIBaseClient


class MSGraphAPIAuthManager:
    def __init__(self, client_id: Text, client_secret: Text, tenant_id: Text, scopes: Optional[List] = None) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.scopes = scopes if scopes else settings.DEFAULT_SCOPES

        self.logger = get_logger(__name__)

    def get_access_token(self):
        return self._execute_ms_graph_api_auth_flow()

    def _get_msal_app(self):
        return msal.PublicClientApplication(
            client_id=self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}"
        )

    def _execute_ms_graph_api_auth_flow(self):
        msal_app = self._get_msal_app()

        device_flow = msal_app.initiate_device_flow(scopes=self.scopes)

        if "user_code" not in device_flow:
            raise ValueError("Failed to create device flow. Err: %s" % json.dumps(device_flow, indent=4))
        
        # TODO: log the message and remove print
        # self.logger.info(device_flow["message"])
        print(device_flow["message"])

        result = msal_app.acquire_token_by_device_flow(device_flow)
        if "access_token" in result:
            # TODO: store access token and refresh token
            return result['access_token']
        else:
            raise AuthException(f'Failed to acquire access token. Error: {result}')

    def _refresh_access_token(self, refresh_token: Text):
        msal_app = self._get_msal_app()

        response = msal_app.acquire_token_by_refresh_token(
            refresh_token=refresh_token,
            scopes=self.scopes,
        )

        return response
    
    def _check_access_token_validity(self, access_token: Text):
        msal_graph_api_client = MSGraphAPIBaseClient(access_token)
        try:
            msal_graph_api_client.check_connection()
            return True
        except Exception as e:
            if 'InvalidAuthenticationToken' in str(e):
                return False
            else:
                raise e