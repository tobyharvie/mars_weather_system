from flask import Flask, request, jsonify
from flask_cors import CORS
# forecasting function using predicter and historical data
from forecasting_model.get_forecast import get_forecast

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from frontend

# API address
@app.route('/api/forecast', methods=['POST'])
def forecast():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON received"}), 400
        forecast = get_forecast(data) # returns a list of dicts
        return jsonify(forecast)
    except Exception as e: return jsonify({'error':str(e)})

# start up server
if __name__ == '__main__':
    app.run(debug=True)