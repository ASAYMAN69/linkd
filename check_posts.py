import asyncio
from scrapling.fetchers import PersistentFetcher

async def check_posts():
    # Check the posts section specifically
    url = "https://www.linkedin.com/in/asayman/recent-activity/posts/"
    print(f"Checking posts at: {url}")
    
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=5000, 
        network_idle=True,
        headless=True 
    )
    
    posts = response.css('.feed-shared-update-v2')
    
    print(f"Found {len(posts)} posts.")
    
    for i, post in enumerate(posts[:3]):
        # Check for any unique identifiers or hidden metadata
        urn = post.attrib.get('data-urn')
        
        # Look for the visual timestamp again, but check if there's a title attribute on the timestamp link
        # often LinkedIn has <a ... title="Wednesday, October 23, 2024, 10:00 AM">
        time_links = post.css('a[href*="/feed/update/urn:li:activity:"]')
        time_title = time_links.attrib.get('title')
        time_aria = time_links.css('span.visually-hidden ::text').get()
        
        print(f"\nPost {i+1}:")
        print(f"  URN: {urn}")
        print(f"  Title attribute: {time_title}")
        print(f"  Visually hidden text: {time_aria.strip() if time_aria else 'N/A'}")
        
        # Check all child elements of the sub-description for a hidden time
        sub_desc = post.css('.update-components-actor__sub-description ::text').getall()
        print(f"  Sub-description pieces: {[s.strip() for s in sub_desc if s.strip()]}")

if __name__ == "__main__":
    asyncio.run(check_posts())
