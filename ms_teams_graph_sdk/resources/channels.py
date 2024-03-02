from typing import Text, Dict, List
from ms_teams_graph_sdk.client.ms_graph_api_base_client import MSGraphAPIBaseClient


class ChannelsResource:
    def __init__(self, client: MSGraphAPIBaseClient) -> None:
        self.client = client
        self._group_ids = None

    def _get_group_ids(self) -> List[Text]:
        """
        Get all group IDs related to Microsoft Teams.

        Returns
        -------
        List[Text]
            The group IDs.
        """

        if not self._group_ids:
            api_url = self.client._get_api_url("groups")
            # only get the id and resourceProvisioningOptions fields
            params = {"$select": "id,resourceProvisioningOptions"}
            groups = self.client._get_response_value_unsafe(self.client._make_request(api_url, params=params))
            # filter out only the groups that are related to Microsoft Teams
            self._group_ids = [item["id"] for item in groups if "Team" in item["resourceProvisioningOptions"]]

        return self._group_ids

    def get_channel(self, group_id: Text, channel_id: Text) -> Dict:
        """
        Get a channel by its ID and the ID of the group that it belongs to.

        Parameters
        ----------
        group_id : str
            The ID of the group that the channel belongs to.

        channel_id : str
            The ID of the channel.

        Returns
        -------
        Dict
            The channel data.
        """

        api_url = self.client._get_api_url(f"teams/{group_id}/channels/{channel_id}")
        channel = self.client._make_request(api_url)

        return channel
    
    def get_channels(self) -> List[Dict]:
        """
        Get all channels.

        Returns
        -------
        List[Dict]
            The channels data.
        """

        channels = []
        for group_id in self._get_group_ids():
            for group_channels in self.client._fetch_data(f"teams/{group_id}/channels", pagination=False):
                channels.extend(group_channels)

        return channels