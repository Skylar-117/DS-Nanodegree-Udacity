import math
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime, date, timedelta

from epx_engagement_model.Config import config

def load_data(patientID, show_dict=False):
    # First: connect the dataase:
    db = mysql.connector.connect(
        user = config.DB_USER,
        password = config.DB_PASSWORD,
        host = config.DB_HOST,
        database = config.DB_NAME
    )
    # Load data from the database, 1 row:
    cur = db.cursor()
    cur.execute(f"select * from {config.DB_TABLE} where patientId={patientID}")
    results = cur.fetchall()
    case = list(results[0])
    case_dict = {}
    for i in range(len(config.FEATURES)):
        case_dict[config.FEATURES[i]] = case[i]
    if(show_dict==True):
        return case_dict
    else:
        return case

def clean_data(data):

    f = pd.DataFrame(data[:-1]).T
    f.columns = config.FEATURES[:-1]

    # Calculate ages:
    today = datetime.strptime("2020-03-02", "%Y-%m-%d")
    dob = (datetime.strptime(f.dob[0], "%Y-%m-%d") if(f.dob[0] is not None) else datetime.strptime("2020-03-02", "%Y-%m-%d"))
    age = ((today - dob)/365.25).days
    f[config.NEW_CREATED_FEATURES_AGE[0]] = (0 if(age<=18) else 1 if((age>18)&(age<=45)) else 2 if((age>45)&(age<=65)) else 3 if((age>65)&(age<=75)) else 4)
    f[config.NEW_CREATED_FEATURES_AGE[1]] = (1 if(age==0) else 0)

    # Rearrange columns order:
    cols = list(f)
    cols.insert(4, cols.pop(cols.index(config.NEW_CREATED_FEATURES_AGE[0])))
    cols.insert(5, cols.pop(cols.index(config.NEW_CREATED_FEATURES_AGE[1])))
    f = f.loc[:, cols]

    # Drop useless columns:
    f.drop(labels=config.DROP_FEATURES[:-1], axis=1, inplace=True)

    # Add zeroDuration columns:
    for pair in config.NEW_CREATED_FEATURES_DURATION:
        f[pair[0]] = (1 if(f[pair[1]] is not None) else 0)

    
    # Add exact intervention columns:
    intervention_name = f.intervention_name[0]
    f.drop(labels=["intervention_name"], axis=1, inplace=True)
    intervention_df = pd.DataFrame()
    for intervention in config.NEW_CREATED_FEATURES_INTERVENTION:
        intervention_df[intervention] = [None]
    if(intervention_name=="epxasthma"):
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[0]] = 1
    elif(intervention_name=="epxcopd"):
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[1]] = 1
    elif(intervention_name=="epxdepress"):
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[2]] = 1
    elif(intervention_name=="epxdiabetes"):
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[3]] = 1
    elif(intervention_name=="epxheart"):
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[4]] = 1
    else:
        intervention_df[config.NEW_CREATED_FEATURES_INTERVENTION[5]] = 1

    f = pd.concat(objs=[f, intervention_df], axis=1) # f will now have 54 columns including dummy-intervention-name

    # Replace None values to np.nan:
    f.fillna(0, inplace=True)
    return f