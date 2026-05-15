import os
import time
from scrapling.fetchers import PersistentFetcher
from scrapling.engines._browsers._stealth import StealthySession

# Define a persistent directory for this project
SESSION_DIR = PersistentFetcher.DEFAULT_SESSION_DIR

def open_persistent_browser():
    print(f"Opening persistent browser with data directory: {SESSION_DIR}")
    
    # We use a session directly to keep the browser open
    # headless=False is the default for this manual task
    with StealthySession(
        headless=False, 
        user_data_dir=SESSION_DIR,
        timeout=0 # Disable timeout for manual login
    ) as session:
        # Get a page and wait for the user
        page_info = session._get_page(timeout=0, extra_headers=None, disable_resources=False)
        page = page_info.page
        page.goto("https://www.google.com")
        
        print("\n" + "="*50)
        print("BROWSER IS OPEN")
        print("Please perform your login or any manual actions.")
        print("The session data (cookies, cache, etc.) will be saved in .scrapling_session")
        print("Close the browser window or press Ctrl+C in this terminal when you are done.")
        print("="*50 + "\n")
        
        try:
            # Keep the script running while the browser is open
            while not page.is_closed():
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")

if __name__ == "__main__":
    open_persistent_browser()
