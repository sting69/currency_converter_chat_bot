from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    if len(target_currency)!=1 :
        response={'fulfillmentText': "Please enter one currency"}
        return jsonify(response)

    cf = fetch_conversion_factor(source_currency, target_currency[0])
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency[0])
    }
    return jsonify(response)


def fetch_conversion_factor(source, target):
    url = 'https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=80084fb9cfa17e0ed24b'.format(source, target)

    response = requests.get(url)
    response = response.json()

    return response['{}_{}'.format(source, target)]


if __name__ == "__main__":
    app.run(debug=True)
