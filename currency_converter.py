import requests

def convert_currency(amount, from_currency, to_currency):
    """
    Convert amount from one currency to another using exchangerate.host API.
    """
    url = f"https://api.exchangerate.host/convert"
    params = {
        "from": from_currency,
        "to": to_currency,
        "amount": amount
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if data.get("success"):
        return data["result"]
    else:
        raise Exception("API conversion failed.")
