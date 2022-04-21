"""Module that contains the make request helper."""
from requests.exceptions import HTTPError

from pybraries.pagination import fix_pages


# pylint: disable=broad-except
def make_request(url: str, kind: str) -> str:
    """Call api server

    Args:
        url (str): base url to call
        kind (str): get, post, put, or delete
    Returns:
        `json` encoded response from libraries.io
    """
    ret = ""
    try:
        params = {"include_prerelease": "False"} if kind == "post" else {}
        fix_pages()  # Must be called before any request for page validation
        resp = getattr(sess, kind)(url, params=params)
        resp.raise_for_status()
        ret = resp.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    finally:
        clear_params()

    return ret
