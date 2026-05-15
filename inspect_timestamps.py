import asyncio
from scrapling.fetchers import PersistentFetcher

async def inspect_timestamps():
    # We check the 'all' activity page which includes posts and comments
    url = "https://www.linkedin.com/in/asayman/recent-activity/all/"
    print(f"Inspecting timestamps at: {url}")
    
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=5000, 
        network_idle=True,
        headless=True 
    )
    
    activities = response.css('.feed-shared-update-v2, [data-urn*="activity"]')
    
    for i, activity in enumerate(activities[:5]):
        # Look for the visual timestamp (e.g., "6mo", "1d")
        # And look for hidden attributes like URNs or accessibility labels which might have precise data
        visual_time = activity.css('.update-components-actor__sub-description .visually-hidden ::text, .update-components-text-view__text-view ::text').get()
        
        # URN often contains a timestamp in some formats, or we can check the 'time' element if it exists
        urn = activity.attrib.get('data-urn')
        
        # Check for any element that might have an aria-label or title with a full date
        detailed_time = activity.css('span[aria-hidden="true"] ::text, .update-components-actor__sub-description ::text').getall()
        
        print(f"\nActivity {i+1}:")
        print(f"  Visual Time: {visual_time.strip() if visual_time else 'N/A'}")
        print(f"  URN: {urn}")
        print(f"  All potential time strings: {detailed_time}")
        
        # Check if there's a specific link to the activity which might have a timestamp in the URL or metadata
        link = activity.css('a.app-aware-link::attr(href)').get()
        print(f"  Link: {link}")

if __name__ == "__main__":
    asyncio.run(inspect_timestamps())
