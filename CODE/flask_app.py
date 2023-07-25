from flask import Flask, request, jsonify, render_template
import pickle
import requests
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    str_features = [str(x) for x in request.form.values()]
    zipcode = str_features[0]
    res,city,weather,temp,zipcode = predict_prob(zipcode)



    return render_template('index.html',
                           prediction_text='You entered zipcode: {}<br>City: {}<br>Current Weather: {}<br>Current temperature: {}F<br>Probability of severity 1: {:.2%} <br> Probability of severity 2: {:.2%}<br> Probability of severity 3: {:.2%}<br> Probability of severity 4: {:.2%}<br> '
                           .format(zipcode,city,weather,temp,res[0],res[1],res[2],res[3])+"""<p style="text-align:center;"><img src="/static/test.png"></p>""")

def predict_prob(zipcode):

    api_key = "3899d4b00889b0c652a8a6506fbfb8a1"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&zip=" + zipcode
    response = requests.get(complete_url)
    result = response.json()
    new_data = pd.DataFrame()
    if "rain" in result.keys():
        new_data['Precipitation(in)'] = result['rain']["1h"]
    else:
        new_data['Precipitation(in)'] = [0]

    temp = round((result['main']['temp'] - 273.15) * 9/5 + 32)

    new_data['Pressure(in)'] = [result["main"]['pressure']/33.864]
    new_data['Visibility(mi)'] = [result["visibility"]/1609]
    new_data['Humidity(%)'] = [result["main"]['humidity']]
    new_data['Wind_Speed(mph)'] = result['wind']['speed']*2.237
    new_data['Early Morning'] =[0]
    new_data['Morning'] =[0]
    new_data['Noon'] =[0]
    new_data['Evening'] =[0]
    new_data['Night'] =[0]
    new_data['Late Night'] =[0]
    x = pd.to_datetime(pd.Timestamp.now()).hour

    if (x > 4) and (x <= 8):
        new_data['Early Morning']= 1
    elif (x > 8) and (x <= 12 ):
        new_data['Morning']=1
    elif (x > 12) and (x <= 16):
         new_data['Noon']=1
    elif (x > 16) and (x <= 20) :
         new_data['Evening']=1
    elif (x > 20) and (x <= 24):
         new_data['Night']=1
    elif (x <= 4):
         new_data['Late Night']=1
    model = pickle.load(open('model.sav', 'rb'))
    prob = [model.predict_proba(new_data)][0][0]

    prob_plot = pd.DataFrame({'Probablity':prob},index = ['Severity 1', 'Severity 2', 'Severity 3','Severity 4'])
    city = result['name']

    weather = result['weather'][0]['main']
    ax = prob_plot.plot.bar(figsize=(10, 8))
    fig = ax.get_figure()
    fig.savefig('static/test.png',dpi=100,bbox_inches = 'tight', facecolor='w',transparent=False)
    return prob,city,weather,temp,zipcode


if __name__ == "__main__":
    app.run()
