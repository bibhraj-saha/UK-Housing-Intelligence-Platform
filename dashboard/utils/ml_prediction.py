from utils.api_client import predict_price


def get_price_prediction(
    average_price: float,
    average_crime: float,
    average_income: float,
):

    features = {
        "average_price": average_price,
        "average_crime": average_crime,
        "average_income": average_income,
    }

    try:

        response = predict_price(features)

        return response

    except Exception as ex:

        return {
            "status": "error",
            "message": str(ex),
        }