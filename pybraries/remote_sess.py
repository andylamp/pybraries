"""Describes the libraries.io session."""
import os
from typing import Optional

import requests
from requests.exceptions import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .errors import APIKeyMissingError, SessionNotInitialisedError


class LibIOSession:
    """
    Class that implements the libraries.io session and keeps its state.
    """

    # session retry settings
    _retry_config = Retry(total=3, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])
    # the libraries.io API key
    _LIBRARIES_API_KEY = os.environ.get("LIBRARIES_API_KEY", None)
    # the default http retry force list set of codes
    default_status_forcelist = {500, 502, 503, 504}
    # the internal session object
    _sess: Optional[requests.Session] = None

    # values used for pagination
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 30

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_session(
        api_key: str = "", force_create: bool = False, include_prerelease: bool = False
    ) -> requests.Session:
        """
        Function that fetches the instantiated session object for libraries.io with desired API key and
        retry config.

        Args:
            api_key (str): The api key to use, if not already set.
            force_create (bool): recreates the session instance.
            include_prerelease (bool): flag that indicates if we enable prerelease or not.

        Returns:
            requests.Session: returns the instantiated session.
        """

        # check if the session exists, if not create it
        if not LibIOSession._sess or force_create:
            # session object common properties
            LibIOSession._sess = requests.Session()
            LibIOSession._sess.mount("https://", HTTPAdapter(max_retries=LibIOSession._retry_config))

        # check if we have an API key
        if api_key:
            LibIOSession.set_key(api_key)

        # check if we need to enable the prerelease flag
        if include_prerelease:
            LibIOSession._sess.params["include_prerelease"] = 1

        # attach the api key to the parameters
        LibIOSession._sess.params["api_key"] = LibIOSession.get_key()

        # finally, return the instantiated session object
        return LibIOSession._sess

    @staticmethod
    def get_key() -> str:
        """
        Function that returns the API key used for the calls.

        Returns:
            str: The API key used for the calls.
        """
        if LibIOSession._LIBRARIES_API_KEY is None or not LibIOSession._LIBRARIES_API_KEY:
            raise APIKeyMissingError(
                "All methods require an API key. "
                "See https://libraries.io to get your free key. "
                "Then set the key to the environment variable: LIBRARIES_API_KEY or pass it as an argument"
            )

        return LibIOSession._LIBRARIES_API_KEY

    @staticmethod
    def set_key(key: str):
        """
        Function that is responsible for setting the internal API key used for the requests.

        Args:
            key (str): the API to set.
        """
        LibIOSession._LIBRARIES_API_KEY = key

    @staticmethod
    def set_retry_config(total: int = 3, backoff_factor: float = 0.2, status_forcelist: Optional[list] = None):
        """
        The retry behaviour to be used for the session.

        Args:
            total (int): the amount of allowed retries.
            backoff_factor (float): the back-off factor.
            status_forcelist (Optional[list]): the http codes that we force retries.
        """
        # check if we have a valid session
        LibIOSession._has_valid_session()

        # now configure the retry parameters
        LibIOSession._retry_config = Retry(
            total=total,
            backoff_factor=backoff_factor,
            status_forcelist=LibIOSession.default_status_forcelist if not status_forcelist else status_forcelist,
        )

        # now add them to the session
        LibIOSession._sess.mount("https://", HTTPAdapter(max_retries=LibIOSession._retry_config))

    # noinspection PyUnresolvedReferences
    @staticmethod
    def clear_session_params():
        """
        Function that clears the session parameters.
        """
        LibIOSession._has_valid_session()

        LibIOSession._sess.params.clear()

    @staticmethod
    def _has_valid_session():
        """
        Function that checks if we have a valid session object - if not, an exception is raised.
        """
        if not LibIOSession._sess:
            raise SessionNotInitialisedError("Session has not been yet initialised, cannot set retry behaviour.")

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def fix_pages(sess: requests.Session, page: Optional[int] = None, per_page: Optional[int] = None) -> bool:
        """
        Change pagination settings.

        :arg
            per_page (Optional[int]): (optional) use this value instead of current session params
            page (Optional[int]): (optional) use this value instead of current session params

        Returns:
            valid_values_range (bool): page and per_page values within valid range
        """
        # try to set the page we want to fetch, the default is the first page (e.g. page = 1)
        try:
            page = sess.params["page"] if page is None else page
        except KeyError:
            page = LibIOSession.DEFAULT_PAGE

        # try to set the items per page we want to get, the default is 30 items per page.
        try:
            per_page = sess.params["per_page"] if per_page is None else per_page
        except KeyError:
            per_page = LibIOSession.DEFAULT_PER_PAGE

        sess.params["page"] = max(page, 1)  # Min value is 1
        sess.params["per_page"] = min(max(per_page, 1), 100)  # Values between 1 and 100

        valid_values_range = sess.params["page"] == page and sess.params["per_page"] == per_page
        return valid_values_range

    # @staticmethod
    # # pylint: disable=broad-except
    # def make_request(url: str, kind: str) -> str:
    #     """Call api server
    #
    #     Args:
    #         url (str): base url to call
    #         kind (str): get, post, put, or delete
    #     Returns:
    #         `json` encoded response from libraries.io
    #     """
    #     ret = ""
    #     try:
    #         params = {"include_prerelease": "False"} if kind == "post" else {}
    #         fix_pages()  # Must be called before any request for page validation
    #         resp = getattr(sess, kind)(url, params=params)
    #         resp.raise_for_status()
    #         ret = resp.json()
    #     except HTTPError as http_err:
    #         print(f"HTTP error occurred: {http_err}")
    #     except Exception as err:
    #         print(f"Other error occurred: {err}")
    #     finally:
    #         clear_params()
    #
    #     return ret
