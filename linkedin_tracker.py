import asyncio
import datetime
import sys
import re
import json
import logging
from scrapling.fetchers import PersistentFetcher

# Suppress scrapling and other logs to ensure clean JSON output
logging.getLogger('scrapling').setLevel(logging.ERROR)

def normalize_url(url):
    """
    Cleans the LinkedIn URL to get the base profile activity URLs.
    """
    url = url.split('?')[0]
    match = re.search(r'(https?://(www\.)?linkedin\.com/in/[^/]+)', url)
    if match:
        base_url = match.group(1).rstrip('/')
        return base_url
    return None

def decode_linkedin_urn(urn):
    """Decodes the millisecond timestamp from a LinkedIn URN."""
    if not urn or ":" not in urn:
        return 0
    try:
        urn_id = int(urn.split(':')[-1])
        return urn_id >> 22
    except Exception:
        return 0

async def get_latest_activity(base_url):
    """Checks all, posts, and comments activity sections and returns the absolute latest one."""
    sections = ["all", "posts", "comments"]
    
    latest_activity = {
        "timestamp": 0,
        "type": None,
        "urn": None,
        "content": None,
        "date_str": None,
        "profile_url": base_url
    }

    for section in sections:
        url = f"{base_url}/recent-activity/{section}/"
        
        response = await PersistentFetcher.async_fetch(
            url, 
            wait=5000, 
            network_idle=True,
            headless=True 
        )
        
        if response.status != 200:
            continue

        activities = response.css('.feed-shared-update-v2, [data-urn*="activity"]')
        
        for activity in activities:
            urn = activity.attrib.get('data-urn')
            ts = decode_linkedin_urn(urn)
            
            if ts > latest_activity["timestamp"]:
                # Extract text more aggressively
                text_elements = activity.css('.update-components-text-view span ::text, .feed-shared-update-v2__description-wrapper ::text, .feed-shared-text ::text, .main-feed-activity-card__commentary ::text').getall()
                content = " ".join([t.strip() for t in text_elements if t.strip() and t.strip().lower() not in ["follow", "•", "3rd+"]])
                
                header = activity.css('.update-components-header__text-view ::text').get()
                header_str = header.strip() if header else ""
                
                if header_str:
                    act_type = header_str
                elif section == "comments":
                    act_type = "Comment"
                elif section == "posts":
                    act_type = "Post"
                else:
                    act_type = "Activity"

                latest_activity.update({
                    "timestamp": ts,
                    "type": act_type,
                    "urn": urn,
                    "content": content[:1000] if content else None,
                    "date_str": datetime.datetime.fromtimestamp(ts/1000.0, datetime.timezone.utc).isoformat()
                })

    return latest_activity

async def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No URL provided"}))
        return

    base_url = normalize_url(sys.argv[1])
    if not base_url:
        print(json.dumps({"error": "Invalid LinkedIn URL"}))
        return

    try:
        result = await get_latest_activity(base_url)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    asyncio.run(main())
