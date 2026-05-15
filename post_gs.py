import requests
import json
import sys
import argparse

def post_to_gs(query_params, body_data):
    # Base URL
    base_url = "https://script.google.com/macros/s/AKfycbwXHyqCX_HxUjjCSIMbQlRGyh33zkrtChw5j1OQKSPUlld6wZUCDEUNj06g1bj7l6li/exec"
    
    # Headers
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    }
    
    # Cookies
    cookies = {
        '__Secure-BUCKET': 'CNAD',
        'SEARCH_SAMESITE': 'CgQIsqAB',
        'HSID': 'A8sCCHnXlek1_V1uw',
        'SSID': 'AoDv6nlTKJ__UdaeB',
        'APISID': 'J9rnsm0wskQzoWuU/AlhAeC9yu7xYoskX8',
        'SAPISID': 'aydcK4epa43g8RKt/Auo2tVZB8iK7ISfN5',
        '__Secure-1PAPISID': 'aydcK4epa43g8RKt/Auo2tVZB8iK7ISfN5',
        '__Secure-3PAPISID': 'aydcK4epa43g8RKt/Auo2tVZB8iK7ISfN5',
        'S': 'billing-ui-v3=J4LYI9Ynq7lYMg58hp9XDXUdZhSa3vls:billing-ui-v3-efe=J4LYI9Ynq7lYMg58hp9XDXUdZhSa3vls',
        'SID': 'g.a0009widvJg328mYMIw1KHgCprKvZIyuhT9qDDxlTtrPWKcyn6xPMYK9m9Kgsqp3EMjUvM1wWwACgYKAQwSARUSFQHGX2MiDG1eguO-zlHKmsV9e2o_ihoVAUF8yKruLNiq-0k2wd5r1QGO8TzB0076',
        '__Secure-1PSID': 'g.a0009widvJg328mYMIw1KHgCprKvZIyuhT9qDDxlTtrPWKcyn6xP28Jm4JQm33BEgrSxJqrhNQACgYKAZwSARUSFQHGX2MidYOU8FMNSIUkCLUTunjGahoVAUF8yKpHHolNzSsDh-vK7y4_dgQ-0076',
        '__Secure-3PSID': 'g.a0009widvJg328mYMIw1KHgCprKvZIyuhT9qDDxlTtrPWKcyn6xPvwU8loeS_MNep3xArI8YNQACgYKAQ8SARUSFQHGX2MiKpoDFe3f3WZfyBNe_FRGsBoVAUF8yKrF0KmG-fkCVfwLkz4ns_YA0076',
        'AEC': 'AaJma5uF4_Zv-0rRCkv0QL4_rkYHjGIpcKK72be9pAwaR5ohzWcOFdzZ-UI',
        'NID': '531=GNATP_BPPxrVkY20pcD94AgkshjNkBK-utHDoEoYeFJsURudpJELFmxaFOXXnR8sgNWCTGxhSS2FX0xpMy-pIQIPuaCeJHuTlDahkqnp5TOXyNoRCHxhwuBNy27ISzF-c1g6iDioLuIMBc8friuK5dQ7WHf4JrXUh-Hpo7B1xVnGrIW87qQdsvs6TvP9IwEUCTaYp_Fg90Ua6z3k51eE4qMGuA8eEHOSz_rup38WPkmxwUeJa82sFiwwxNZA_XtUTIy68Mc4DJUrgOP-pidMyoF6wWeaftTSY1HfqmL4Iol2U02sgJzbU3iGJ2HQ9nr80lxEm6bwVXoS00i6EsKloz06r9iGpKyZiGRa1PKZABw78BgOqT4T8bQG_L31-p8_lH_U4uDW6w',
        '__Secure-1PSIDTS': 'sidts-CjEBhkeRd2vy3A6IP0fZ2nNVpO_AIb_1BIgLYxBw3o97Mr1CMH4r_vIWQVAJjw_S7U9nEAA',
        '__Secure-3PSIDTS': 'sidts-CjEBhkeRd2vy3A6IP0fZ2nNVpO_AIb_1BIgLYxBw3o97Mr1CMH4r_vIWQVAJjw_S7U9nEAA',
        'COMPASS': 'appsdev-apps-platform-console-ui=CgAQpN6d0AYafQAJa4lXmc11eUaTCzjklu1hIIhxkOi1LKsoCt1wyC_TQhUBnkRQryow3t2zLQ_yctNVDbbNOJAHyU2wqH-XCe_rKEVep0LseMVKft5lG2QqIKRTsZ-tmGfj1gg4TlmWcc5Yf4FI-bY9EJ6g-veRpjz66ZZ-pri-sjEdI2aAMAE',
        '_gid': 'GA1.3.708827492.1778868503',
        '_ga': 'GA1.1.1103385103.1778868502',
        'OTZ': '8609408_32_32__32_',
        '_ga_60Q1X42Z2X': 'GS2.1.s1778868501$o1$g1$t1778868732$j60$l0$h0',
        '_ga_S6TL92G5N1': 'GS2.1.s1778868503$o1$g1$t1778868732$j60$l0$h0',
        'SIDCC': 'AKEyXzUlR-FMSnEg_stE3M1CFbe4vU-mzjdYex-pRac28YZ-lKfbClGD8Gn6FOiQP1TF6XBaRcC9',
        '__Secure-1PSIDCC': 'AKEyXzUsDPhnKPTWGTTIKlHz4FgLv9GvA2MNYRuXcNdgk5KUparWHDljb4JtA9l1SynoL36gH8o',
        '__Secure-3PSIDCC': 'AKEyXzWS5MkrsWv3e1XZeZQEGs8yQDX8cbzxC4P_pqdv2NZLGOtJ3qOWXkD1No3PAVSklpgg-F4'
    }

    print(f"Sending POST request...")
    if query_params:
        print(f"Query Params: {query_params}")
    if body_data:
        print(f"Body Data: {json.dumps(body_data, indent=2)}")

    response = requests.post(base_url, params=query_params, headers=headers, cookies=cookies, json=body_data)
    
    if response.status_code == 200:
        print("Response received:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    else:
        print(f"Error: Status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send dynamic POST request to Google Apps Script.')
    parser.add_argument('-p', '--params', nargs='*', help='Query parameters as key=value pairs (e.g., id=123 type=update)')
    parser.add_argument('-b', '--body', help='JSON body as a string (e.g., \'{"name": "Ayman", "age": 25}\')')

    args = parser.parse_args()

    # Parse query parameters
    query_dict = {}
    if args.params:
        for item in args.params:
            if '=' in item:
                key, value = item.split('=', 1)
                query_dict[key] = value

    # Parse body
    body_dict = {}
    if args.body:
        try:
            body_dict = json.loads(args.body)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON body: {e}")
            sys.exit(1)

    post_to_gs(query_dict, body_dict)
