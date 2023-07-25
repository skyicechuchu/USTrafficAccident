Description
Traffic accidents have been a leading cause of deaths and severe injuries in the U.S., lead to heavy financial losses, and have been a key public safety challenge. We use big dataset to create three main components historical accident dashboard, severe accidents probability heatmap and real-time accidents severity predictions. We combined 1 linear and 2 non-linear ML models and used various feature engineering, overfitting reduction techniques and achieved high prediction accuracy.We designed a web application with interactive visualizations to help draw insights from historical data, and assess the risk of experiencing severe traffic accident in real time


Installation
There are no need extra package needed. We implement on pythonanywhere as a webpage to let user operate. 

Execution
How to Run the Flask Application
*Web application can be also found on http://6242team108.pythonanywhere.com/ without hosting local server by steps bellow

1. Run the flask_app.py using python or "Flask APP.ipynb" in Jupyter notebook.
2. The default flask server should be http://127.0.0.1:5000/, open it in incognito mode for best result.
3. Enter a valid zip code.
4. Prediction will be generated base on live weather data.
