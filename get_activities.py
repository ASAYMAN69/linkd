import asyncio
from scrapling.fetchers import PersistentFetcher
from scrapling.core.utils import log

async def get_linkedin_activities():
    url = "https://www.linkedin.com/in/asayman/recent-activity/all/"
    print(f"Fetching activities from: {url}")
    
    # Use PersistentFetcher to leverage the logged-in session
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=8000, 
        network_idle=True,
        headless=True 
    )
    
    if response.status != 200:
        print(f"Failed to fetch page. Status code: {response.status}")
        return

    # Extract activities using the verified selector
    activities = response.css('.feed-shared-update-v2, [data-urn*="activity"]')
    
    print(f"\nSuccessfully found {len(activities)} recent activities for AS Ayman.\n")
    print("="*60)
    
    for i, activity in enumerate(activities):
        # Header: Who did what (e.g., "AS Ayman reposted this")
        header = activity.css('.update-components-header__text-view ::text').get()
        header = header.strip() if header else "Original Post"
        
        # Metadata: Date and actor info
        subtext_elements = activity.css('.update-components-actor__sub-description ::text').getall()
        date = " ".join([s.strip() for s in subtext_elements if s.strip()])
        
        # We'll use a more reliable approach: get all text but filter out the common noise
        all_text = activity.css('::text').getall()
        content_parts = []
        
        # Heuristic: skip text until we see the date/time, then collect long strings
        # or just filter out known UI noise
        noise = ["follow", "•", "3rd+", "activate to view larger image", "feed post number", "as ayman"]
        
        capture = False
        for t in all_text:
            t_clean = t.strip()
            if not t_clean: continue
            
            # Simple date heuristic to start capturing
            if any(x in t_clean.lower() for x in ["mo", "yr", "h", "d"]) and len(t_clean) < 10:
                capture = True
                continue
            
            if capture:
                if not any(n in t_clean.lower() for n in noise) and len(t_clean) > 10:
                    content_parts.append(t_clean)

        content = " ".join(content_parts)

        print(f"ACTIVITY {i+1}")
        print(f"Type: {header}")
        if date:
            print(f"Time: {date}")
        print("-" * 20)
        if content:
            # Clean up and show
            content = " ".join(content.split())
            print(f"{content[:500]}...") # Show more content
        else:
            # Last ditch effort: show first few long words if heuristic failed
            fallback = [t.strip() for t in all_text if len(t.strip()) > 30 and not any(n in t.lower() for n in noise)]
            if fallback:
                print(" ".join(fallback)[:500] + "...")
            else:
                print("[Media post, repost without comment, or content not found]")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(get_linkedin_activities())
