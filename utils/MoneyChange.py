import requests
from config_keys import MONEY_CHANGE_API_KEY

def obtain_money_change():
    """
    Fetch the USD to EUR exchange rate from CurrencyLayer API.

    Returns:
        float: Exchange rate EUR -> USD if successful, None otherwise.
    """

    url = f"http://api.currencylayer.com/live"
    parameter = {'access_key': MONEY_CHANGE_API_KEY, 'currencies': "USD", 'source': "EUR"}

    try:
        response = requests.get(url, params=parameter)
        response.raise_for_status()  # Exception if error HTTP
        return response.json()["quotes"]["EURUSD"]
    except (requests.RequestException, KeyError) as e:
        print(f"Error al obtener el tipo de cambio: {e}")
        return None