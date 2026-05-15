import asyncio
from scrapling.fetchers import PersistentFetcher
import datetime

def decode_linkedin_urn(urn):
    """
    Decodes the timestamp from a LinkedIn URN.
    LinkedIn URNs for activities are often 64-bit integers where the first 
    41 bits are the timestamp in milliseconds since the epoch.
    """
    if not urn or ":" not in urn:
        return None
    
    try:
        # Extract the ID from urn:li:activity:XXXXXXXXXXXXXXXXXXX
        urn_id = int(urn.split(':')[-1])
        # The timestamp is the first 41 bits (approximately)
        # We shift right by 22 bits
        timestamp_ms = urn_id >> 22
        # Convert to seconds
        timestamp_s = timestamp_ms / 1000.0
        return datetime.datetime.fromtimestamp(timestamp_s, datetime.timezone.utc)
    except Exception as e:
        print(f"Error decoding URN {urn}: {e}")
        return None

async def verify_urn_timestamps():
    url = "https://www.linkedin.com/in/asayman/recent-activity/all/"
    print(f"Verifying timestamps at: {url}")
    
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=5000, 
        network_idle=True,
        headless=True 
    )
    
    activities = response.css('.feed-shared-update-v2, [data-urn*="activity"]')
    
    print(f"\nFound {len(activities)} activities with URNs.")
    
    for i, activity in enumerate(activities):
        urn = activity.attrib.get('data-urn')
        visual_time = activity.css('.update-components-actor__sub-description ::text').get()
        visual_time = visual_time.strip() if visual_time else "N/A"
        
        precise_time = decode_linkedin_urn(urn)
        
        print(f"\nActivity {i+1}:")
        print(f"  URN: {urn}")
        print(f"  Relative (UI): {visual_time}")
        if precise_time:
            print(f"  Decoded Precise Time: {precise_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        else:
            print("  Decoded Precise Time: FAILED")

if __name__ == "__main__":
    asyncio.run(verify_urn_timestamps())
