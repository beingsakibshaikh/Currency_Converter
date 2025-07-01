import requests
from django.shortcuts import render
from django.http import JsonResponse

# Fetch currencies from CoinGecko
def get_all_currencies():
    coingecko_url = "https://api.coingecko.com/api/v3/coins/list"
    fiat_url = "https://open.er-api.com/v6/latest/USD"

    try:
        crypto_data = requests.get(coingecko_url).json()
        fiat_response = requests.get(fiat_url).json()

        fiat_data = fiat_response.get("rates", {})
        fiats = {code.upper(): f"{code.upper()} Currency" for code in fiat_data.keys()}
        coins = [{"id": coin["id"], "name": coin["name"], "type": "crypto"} for coin in crypto_data]

        return fiats, coins
    except Exception:
        return {}, []

# Load and store currencies globally
fiats, coins = get_all_currencies()

# Homepage
def home(request):
    currency_data = [
        {"code": code.lower(), "name": name, "flag": f"https://flagcdn.com/24x18/{code[:2].lower()}.png"}
        for code, name in fiats.items()
    ] + [
        {"code": coin["id"], "name": coin["name"], "flag": f"https://cryptologos.cc/logos/{coin['id']}-logo.png?v=1"}
        for coin in coins
    ]
    return render(request, "converter/home.html", {"currency_data_json": currency_data})

# Conversion route (called via JS)
def convert_currency(request):
    from_currency = request.GET.get("from")
    to_currency = request.GET.get("to")
    amount = float(request.GET.get("amount", 0))

    try:
        # CoinGecko conversion
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": from_currency,
            "vs_currencies": to_currency
        }
        response = requests.get(url, params=params)
        data = response.json()

        result = data.get(from_currency, {}).get(to_currency)
        if result:
            converted = result * amount
            return JsonResponse({"result": f"{converted:.2f}"})
        else:
            return JsonResponse({"error": "Conversion failed."})
    except Exception as e:
        return JsonResponse({"error": str(e)})
