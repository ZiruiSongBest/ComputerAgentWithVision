import asyncio
from gemini_webapi import GeminiClient

# Replace "COOKIE VALUE HERE" with your actual cookie values.
# Leave Secure_1PSIDTS empty if it's not available for your account.
Secure_1PSID = "__Secure-1PSIDCC=AKEyXzWXux4spfIEmcJvIEXKgSwbtH0ZZOabGxiY0hfbVMw6psyrljk74_q6vieSuWVuH3gxjA; expires=Mon, 14-Apr-2025 07:04:40 GMT; path=/; domain=.google.com; Secure; HttpOnly; priority=high"
Secure_1PSIDTS = "COOKIE VALUE HERE"

async def main():
    # If browser-cookie3 is installed, simply use `client = GeminiClient()`
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxies=None)
    await client.init(timeout=30, auto_close=False, close_delay=300, auto_refresh=True)

    response2 = await client.generate_content("@Youtube https://www.youtube.com/watch?v=Qofdx9tEWBw Where is Ken right now?")
    print(response2, "\n\n----------------------------------\n")

asyncio.run(main())

asyncio.run(main())