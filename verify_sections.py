import asyncio
import json
import logging
from scrapling.fetchers import PersistentFetcher

# Suppress scrapling logs
logging.getLogger('scrapling').setLevel(logging.ERROR)

def decode_linkedin_urn(urn):
    if not urn or ":" not in urn:
        return 0
    try:
        urn_id = int(urn.split(':')[-1])
        return urn_id >> 22
    except Exception:
        return 0

async def check_section(base_url, section):
    url = f"{base_url}/recent-activity/{section}/"
    print(f"DEBUG: Checking {url}")
    
    response = await PersistentFetcher.async_fetch(
        url, 
        wait=5000, 
        network_idle=True,
        headless=True 
    )
    
    activities = response.css('.feed-shared-update-v2, [data-urn*="activity"]')
    results = []
    for activity in activities:
        urn = activity.attrib.get('data-urn')
        ts = decode_linkedin_urn(urn)
        results.append({"urn": urn, "ts": ts})
    
    return results

async def verify_sections(profile_name):
    base_url = f"https://www.linkedin.com/in/{profile_name}"
    
    sections = ["all", "posts", "comments"]
    all_data = {}
    
    for section in sections:
        all_data[section] = await check_section(base_url, section)
        print(f"Found {len(all_data[section])} items in {section}")
    
    # Compare
    all_urns = {item["urn"] for item in all_data["all"]}
    post_urns = {item["urn"] for item in all_data["posts"]}
    comment_urns = {item["urn"] for item in all_data["comments"]}
    
    print("\nComparison:")
    print(f"Unique URNs in 'all': {len(all_urns)}")
    print(f"Unique URNs in 'posts': {len(post_urns)}")
    print(f"Unique URNs in 'comments': {len(comment_urns)}")
    
    combined = all_urns | post_urns | comment_urns
    print(f"Total unique URNs combined: {len(combined)}")
    
    missing_from_all = combined - all_urns
    if missing_from_all:
        print(f"WARNING: 'all' section is missing {len(missing_from_all)} items found in other sections!")
        for urn in missing_from_all:
            print(f"  Missing URN: {urn}")
    else:
        print("SUCCESS: 'all' section contains everything found in posts and comments.")

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "tasinmid"
    asyncio.run(verify_sections(name))
