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


def get_serving_health():

    response = requests.get(
        f"{API_BASE_URL}/serving/health",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def get_available_areas():

    response = requests.get(
        f"{API_BASE_URL}/serving/areas",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_area_prediction(
    lsoa_code: str,
):

    response = requests.get(
        f"{API_BASE_URL}/serving/{lsoa_code}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_price_prediction(
    lsoa_code: str,
):

    response = requests.get(
        f"{API_BASE_URL}/serving/{lsoa_code}/price",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_growth_prediction(
    lsoa_code: str,
):

    response = requests.get(
        f"{API_BASE_URL}/serving/{lsoa_code}/growth",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_investment_prediction(
    lsoa_code: str,
):

    response = requests.get(
        f"{API_BASE_URL}/serving/{lsoa_code}/investment",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_recommendation(
    lsoa_code: str,
):

    response = requests.get(
        f"{API_BASE_URL}/serving/{lsoa_code}/recommendation",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()