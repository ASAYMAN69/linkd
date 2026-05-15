import asyncio
from scrapling.fetchers import PersistentFetcher

async def check_comments():
    # Check the comments section specifically
    url = "https://www.linkedin.com/in/asayman/recent-activity/comments/"
    print(f"Checking comments at: {url}")
    
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=5000, 
        network_idle=True,
        headless=True 
    )
    
    # Comments usually have a different structure
    # They are often wrapped in 'main-feed-activity-card' or similar
    comment_cards = response.css('.main-feed-activity-card, .feed-shared-update-v2')
    
    print(f"Found {len(comment_cards)} comment/activity cards.")
    
    for i, card in enumerate(comment_cards[:5]):
        # Look for time specifically in comments
        time_text = card.css('.main-feed-activity-card__subtext ::text, .update-components-actor__sub-description ::text').getall()
        time_text = [t.strip() for t in time_text if t.strip()]
        
        # Check for any span with 'visually-hidden' which often contains the full date/time
        hidden_times = card.css('.visually-hidden ::text').getall()
        
        print(f"\nCard {i+1}:")
        print(f"  Time text: {time_text}")
        print(f"  Hidden text: {hidden_times[:10]}...") # First 10 bits

if __name__ == "__main__":
    asyncio.run(check_comments())
