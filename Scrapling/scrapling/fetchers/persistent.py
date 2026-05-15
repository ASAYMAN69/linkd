import os
from scrapling.fetchers.stealth_chrome import StealthyFetcher
from scrapling.engines._browsers._types import StealthSession
from scrapling.core._types import Unpack
from scrapling.engines.toolbelt.custom import Response

class PersistentFetcher(StealthyFetcher):
    """A Fetcher that uses a project-persistent Chromium session.
    
    This fetcher is pre-configured to store and load cookies, cache, and other 
    session data from a local directory, ensuring persistence across project restarts.
    """
    
    # Default session directory relative to the project root
    DEFAULT_SESSION_DIR = os.path.join(os.getcwd(), ".scrapling_session")

    @classmethod
    def fetch(cls, url: str, **kwargs: Unpack[StealthSession]) -> Response:
        """Fetch using the persistent session."""
        if "user_data_dir" not in kwargs:
            kwargs["user_data_dir"] = cls.DEFAULT_SESSION_DIR
            
        return super().fetch(url, **kwargs)

    @classmethod
    async def async_fetch(cls, url: str, **kwargs: Unpack[StealthSession]) -> Response:
        """Fetch asynchronously using the persistent session."""
        if "user_data_dir" not in kwargs:
            kwargs["user_data_dir"] = cls.DEFAULT_SESSION_DIR
            
        return await super().async_fetch(url, **kwargs)
