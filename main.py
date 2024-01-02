import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta
from pprint import pprint

CURRENCIES = ["EUR", "USD"]
MAX_ALLOWED_DAYS = 10


def get_links(days_range):
    link_base = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
    links = []
    now = datetime.now()

    for day in range(days_range):
        date = (now - timedelta(days=day)).strftime("%d.%m.%Y")
        link = link_base + date
        links.append(link)

    return links


async def main_func(links, currencies):
    async with aiohttp.ClientSession() as session:
        result = []
        for link in links:
            async with session.get(link) as response:
                try:
                    if response.status == 200:
                        json_resp = await response.json()
                        date = link[-10:]
                        vrapper_dct = {}
                        vrapper_dct[date] = {}

                        for cur_data in json_resp["exchangeRate"]:
                            if cur_data["currency"] in currencies:
                                vrapper_dct[date][cur_data["currency"]] = {
                                    "sale": cur_data["saleRate"],
                                    "purchase": cur_data["purchaseRate"],
                                }

                        result.append(vrapper_dct)

                    else:
                        print(f"Error status: {response.status}")
                except aiohttp.ClientConnectorError as e:
                    print(f"Connection error:", str(e))

        return result


if __name__ == "__main__":
    while True:
        try:
            days = int(input("Enter number of days to show(1-10) --> "))
            if 1 <= days <= MAX_ALLOWED_DAYS:
                links = get_links(days)
                res = asyncio.run(main_func(links, CURRENCIES))
                pprint(res)
                break
            else:
                print("I can only show result for the last 10 days!")
        except ValueError:
            print("Please enter a valid integer for the number of days.")