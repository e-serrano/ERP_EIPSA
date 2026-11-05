import requests
from config.config_keys import MONEY_CHANGE_API_KEY

def obtain_money_change():
    """
    Fetch the USD to EUR exchange rate from CurrencyLayer API.

    Returns:
        float: Exchange rate EUR -> USD if successful, None otherwise.
    """

    url = "https://api.frankfurter.dev/v2/rate/eur/usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return float(response.json()["rate"])

    except (requests.RequestException, KeyError, TypeError, ValueError) as e:
        print(f"Error al obtener el tipo de cambio: {e}")
        return None

    # url = f"https://api.exchangerate.host/live"
    # parameters = {
    #     "access_key": MONEY_CHANGE_API_KEY,
    #     "base": "EUR",
    #     "symbols": "USD"
    # }

    # try:
    #     response = requests.get(
    #         url,
    #         params=parameters,
    #         timeout=10
    #     )

    #     response.raise_for_status()
    #     data = response.json()

    #     if not data.get("success"):
    #         print(f"API error: {data.get('error')}")
    #         return None

    #     return float(data["rates"]["USD"])

    # except (requests.RequestException, KeyError, TypeError, ValueError) as e:
    #     print(f"Error al obtener el tipo de cambio: {e}")
    #     return None