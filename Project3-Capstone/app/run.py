
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import mysql.connector
import shap

from flask import Flask, send_file
from flask import render_template, request, jsonify
import io
import base64
import urllib.parse

from epx_engagement_model.Config import config
from epx_engagement_model.data import process_data
from epx_engagement_model.model import predict

app = Flask(__name__)

# Connect database:
db = mysql.connector.connect(
        user = config.DB_USER,
        password = config.DB_PASSWORD,
        host = config.DB_HOST,
        database = config.DB_NAME
    )

# Load model:
model = joblib.load('/Users/dan/Code/Interventions/Model_Artifacts/flask/app/epx_engagement_model/model/pp_lgb.pkl')

# web page that handles user query and displays model results
@app.route('/')
def index():
    return render_template('master.html')

@app.route('/go')
def go():

    # save user input in query
    pid_query = request.args.get('pid', '') 

    # Load data:
    cur = db.cursor()
    cur.execute(f"select * from {config.DB_TABLE} where patientId={pid_query}")
    
    # Convert to json format:
    results_json = []
    header = [i[0] for i in cur.description]
    results = cur.fetchall()
    for i in results:
        results_json.append(dict(zip(header, i)))

    # Clean data:
    patient = list(results[0])
    patient_clean = process_data.clean_data(data=patient)

    # Data transform:
    X_transformed = predict.transform_data(model=model, X=patient_clean)

    # Prediction:
    pred = predict.prediction(model=model, X=X_transformed)
    
    # Model insights:
    decision = predict.model_decision(pred=pred)

    # Risk:
    risk = 'dropping off' if(pred[0][0]<0.5) else 'engaged'

    # SHAP force_plot in html format:
    shap_plot = predict.shap_plot(model=model, X=X_transformed)
    shap.save_html('../app/templates/shap.html', shap_plot)

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        results = results_json[0],
        # decision = decision,
        pred=f'{round(pred[0][0]*100,3)}%',
        risk=risk
        # query=query
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)