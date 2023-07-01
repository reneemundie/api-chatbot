from flask import Flask, render_template, jsonify, request
import api as api
import chatbot as cb

# Creating the application object
app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        response = cb.start_chat(data)
        return jsonify({'response': str(response)})
    else:
        return render_template('index.html')

weather_data = api.get_weather_data()

@app.route('/data')
def json_weather():
    return jsonify(weather_data)

# Function to format the JSON weather data to Python dictionary and route it to /pydata path
@app.route('/pydata')
def python_weather():
    py_data = api.py_weather_data()
    return py_data

# Main function to run the application on port 8000
if __name__ == '__main__':
    app.run(debug=True, port=8000)