# subscribe_api.py
from typing import Any

from pybraries.subscription_helpers import sub_api


class Subscribe:
    """Class for libraries.io API for changing user's libraries.io subscriptions"""

    @staticmethod
    def list_subscribed() -> Any:
        """
        Return a list of packages a user is subscribed to for release notifications.

        Returns:
            Dict with info for each package subscribed to at libraries.io.
        """
        return sub_api("list_subscribed")

    @staticmethod
    def subscribe(manager: str, package: str) -> str:
        """
        Subscribe to receive notifications about new releases of a project.

        Not working yet, but hope to include - possible bug at libraries.io:
        include_prerelease: default = True. Include prerelease notifications.

        Args:
            manager: package manager name (e.g. PyPI).
            package: package name.
        Returns:
            Subscription confirmation message.
        """
        return str(sub_api("subscribe", manager, package))

    @staticmethod
    def check_subscribed(manager: str, package: str) -> bool:
        """
        Check if a user is subscribed to notifications for new project releases.

        Args:
            manager: package manager name (e.g. PyPI).
            package: package name.
        Returns:
            True if subscribed to the package indicated, else False.
        """
        return bool(sub_api("check_subscribed", manager, package))

    @staticmethod
    def update_subscribe(manager: str, package: str, include_prerelease: bool = True) -> str:
        """
        NOT IMPLEMENTED due to possible bug in libraries.io
        Update the options for a subscription.

        Args:
            manager: package manager name (e.g. PyPI).
            package: package name.
            include_prerelease (bool): default = True. Include prerelease notifications.

        Returns:
            Update confirmation message.
        """
        return str(sub_api("update_subscribe", manager, package, include_prerelease))

    @staticmethod
    def unsubscribe(manager: str, package: str) -> str:
        """
        Stop receiving release notifications from a project.

        Args:
            manager: package manager name (e.g. PyPI).
            package: package name.

        Returns:
            Message confirming deleted or deletion unnecessary.
        """

        return str(sub_api("delete_subscribe", manager, package))
