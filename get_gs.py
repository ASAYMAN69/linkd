import requests
import json

def run_webhook_flow():
    # The first webhook URL
    first_url = "https://script.google.com/macros/s/AKfycbx6oX9ALlbrgHqTZc3Xyoy9cAUR_t3FrzkBrw6vflfD6WAQrPlx1p7H_pGWqThegz0g/exec"
    
    # Headers for the first request (as provided in the prompt)
    # Note: Some headers like 'x-client-data' are browser-specific and might expire or be rejected by Google if stale,
    # but we include them as they were in the original curl.
    headers_1 = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-BD,en;q=0.9,bn-BD;q=0.8,bn;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-form-factors': '"Desktop"',
        'sec-ch-ua-full-version': '"148.0.7778.96"',
        'sec-ch-ua-full-version-list': '"Chromium";v="148.0.7778.96", "Google Chrome";v="148.0.7778.96", "Not/A)Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '""',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'x-browser-channel': 'stable',
        'x-browser-copyright': 'Copyright 2026 Google LLC. All Rights Reserved.',
        'x-browser-validation': 'EP+rKgBnotwNixT4iWHNTxTsgCU=',
        'x-browser-year': '2026',
        'x-client-data': 'CI+2yQEIpbbJAQipncoBCKn+ygEIlqHLAQiHoM0BCIi+zwEIx7/PAQiWws8BCMbGlDAI/saUMAjMx5QwCOPHlDAIx8iUMA=='
    }
    
    # Cookies for the first request
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

    print(f"Step 1: Requesting first webhook...")
    # We disable automatic redirect to capture the second URL manually
    response_1 = requests.get(first_url, headers=headers_1, cookies=cookies, allow_redirects=False)
    
    if response_1.status_code == 302:
        second_url = response_1.headers.get('Location')
        print(f"Captured second webhook URL: {second_url}")
        
        # Step 2: Request the second URL
        # The user provided slightly different headers for the second call (no cookies)
        headers_2 = headers_1.copy()
        # Remove browser specific headers that might cause issues on the redirect domain if strictly validated
        # but the user's curl had them, so we keep them.
        
        print(f"Step 2: Requesting second webhook...")
        response_2 = requests.get(second_url, headers=headers_2) # Cookies are NOT usually sent to googleusercontent.com
        
        if response_2.status_code == 200:
            print("Successfully retrieved data!")
            print("Response content:")
            print(response_2.text)
            return response_2.text
        else:
            print(f"Error on Step 2: Status code {response_2.status_code}")
            print(response_2.text)
    else:
        print(f"Error on Step 1: Expected 302 redirect, got {response_1.status_code}")
        print(response_1.text)

if __name__ == "__main__":
    run_webhook_flow()
