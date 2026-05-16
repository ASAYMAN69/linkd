import asyncio
import json
import datetime
import sys
import os
import urllib.request
from get_gs import run_webhook_flow
from post_gs import post_to_gs

# Try to load Telegram credentials
try:
    from api_key import BOT_TOKEN
    with open('chat_id.txt', 'r') as f:
        CHAT_ID = f.read().strip()
except ImportError:
    BOT_TOKEN = None
    CHAT_ID = None
except FileNotFoundError:
    CHAT_ID = None

def send_telegram_alert(message):
    """Sends a message to Telegram if credentials are set."""
    if not BOT_TOKEN or not CHAT_ID or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")

async def run_linkedin_script(semaphore, row, today_str):
    async with semaphore:
        linkedin_url = str(row.get('linkedin'))
        print(f"[*] Processing {linkedin_url}...")
        
        # Run linkedin_tracker.py as a subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable, 'linkedin_tracker.py', linkedin_url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            print(f"[!] Error running tracker for {linkedin_url}: {stderr.decode()}")
            return

        try:
            result = json.loads(stdout.decode())
            if "error" in result:
                print(f"[!] Tracker returned error for {linkedin_url}: {result['error']}")
                return
            
            last_post = result.get('date_str') # Using the datestamp as the "last post" value
            if not last_post:
                print(f"[!] No date_str found for {linkedin_url}")
                return

            print(f"[+] Found last post timestamp for {linkedin_url}: {last_post}")
            
            # --- TELEGRAM ALERT LOGIC ---
            # Check if activity happened in the last 24 hours
            ts_ms = result.get('timestamp', 0)
            now_ms = datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000
            if ts_ms > (now_ms - 24 * 60 * 60 * 1000):
                print(f"[*] Sending Telegram alert for {linkedin_url}...")
                msg = f"🔔 <b>New LinkedIn Activity!</b>\n\n" \
                      f"<b>Profile:</b> {linkedin_url}\n" \
                      f"<b>Type:</b> {result.get('type')}\n" \
                      f"<b>Time:</b> {last_post}\n\n" \
                      f"<b>Content Preview:</b>\n{result.get('content')[:200]}..."
                send_telegram_alert(msg)
            # ----------------------------

            # Prepare update for post_gs.py
            query_params = {'linkedin': linkedin_url}
            body_data = {
                'last_post': last_post,
                'status': today_str
            }
            
            print(f"[*] Updating GS for {linkedin_url}...")
            # We call the function directly from post_gs.py
            post_to_gs(query_params, body_data)
            
        except json.JSONDecodeError:
            print(f"[!] Failed to parse tracker output for {linkedin_url}: {stdout.decode()}")

async def main():
    try:
        # 1. Get today's date
        today_str = datetime.date.today().isoformat()
        print(f"[*] {datetime.datetime.now()}: Starting daily check for {today_str}")

        # 2. Get data from get_gs.py
        print("[*] Fetching data from Google Sheets...")
        try:
            data_str = run_webhook_flow()
        except Exception as e:
            print(f"[!] CRITICAL: get_gs.py failed to run: {e}")
            return

        if not data_str:
            print("[!] Failed to fetch data (empty response).")
            return

        try:
            # Clean data_str in case it has leading/trailing whitespace or non-json junk
            data_str = data_str.strip()
            # If the output contains other print statements, try to find the JSON part
            if not data_str.startswith('[') and '[' in data_str:
                 data_str = data_str[data_str.find('['):]
            
            rows = json.loads(data_str)
        except json.JSONDecodeError as e:
            print(f"[!] Failed to parse data from Google Sheets as JSON.")
            print(f"[!] Raw data received: {data_str[:500]}...")
            print(f"[!] Error: {e}")
            return

        if not isinstance(rows, list):
            print(f"[!] Expected a list of rows, but got {type(rows).__name__}")
            return

        # 3. Filter rows and run tasks
        tasks = []
        semaphore = asyncio.Semaphore(3) # Max 3 parallel executions
        
        for row in rows:
            if not isinstance(row, dict): continue
            
            linkedin = row.get('linkedin')
            status = row.get('status')
            
            if not linkedin:
                continue
                
            # If status is not today's date, we need to check it
            if str(status) != today_str:
                tasks.append(run_linkedin_script(semaphore, row, today_str))

        if not tasks:
            print("[*] No rows need updating today.")
            return

        print(f"[*] Queuing {len(tasks)} profiles for checking...")
        await asyncio.gather(*tasks)
        print(f"[*] {datetime.datetime.now()}: All tasks completed successfully.")

    except Exception as e:
        print(f"[!] UNEXPECTED CRASH in orchestrator.py: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
