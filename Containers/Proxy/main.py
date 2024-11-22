#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 22/11/24.
#

from flask import Flask, make_response, abort, request, jsonify

app = Flask( __name__)

# GET /watch/ticker
# GET /watch/ticker?avg=<num>
@app.route('/watch/<ticker>', methods=['GET'])
def watch_get_ticker(ticker):
    average = request.args.get("avg")
    if average is None:
        # TODO: Fetch and return last value
        print("WATCH " + ticker)
        return make_response('', 204) # No Content
    else:
        try:
            n = int(average)
            # TODO: Fetch last n values
            # TODO: Compute and return average
            print("WATCH average (" + str(n) + ") of " + ticker)
            return make_response('', 204) # No Content
        except:
            abort(400) # Bad Request

# PUT /user/email
# -- ticker
@app.route('/user/<email>', methods=['PUT'])
def user_put_user_data(email):
    content_length = request.content_length
    if content_length is None:
        abort(400) # Bad Request
    if content_length > 16:
        # Twice the length of NASDAQ's maximum ticker symbol length (8)
        # https://www.nasdaqtrader.com/Trader.aspx?id=StockSymChanges
        abort(413) # Content Too Large 
    ticker = request.get_data(as_text=True)
    # TODO: Check email (?)
    # TODO: UPSERT in DB
    print("PUT " + email + " for " + ticker)
    return make_response('', 204) # No Content

# DELETE /user/email
@app.route('/user/<email>', methods=['DELETE'])
def user_delete_user_data(email):
    # TODO: Check email (?)
    # TODO: Delete from DB
    print("DELETE " + email)
    return make_response('', 204) # No Content

# data = request.get_json()
# Example usage: data['owner']['first_name']

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=80)