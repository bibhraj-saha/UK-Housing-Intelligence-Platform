import requests


API_BASE_URL = "http://127.0.0.1:8000"


def check_api_connection():

    try:

        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5,
        )

        return response.status_code == 200

    except Exception:

        return False


def get_api_status():

    response = requests.get(
        f"{API_BASE_URL}/health",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


def predict_price(features: dict):

    response = requests.post(
        f"{API_BASE_URL}/prediction",
        json=features,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()