import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Transform data (scaler + PCA):
def transform_data(model, X):
    # For pipelined estimators:
    data_normalized = model["scaler"].transform(X)
    data_reduced = model["pca_8"].transform(data_normalized)
    return data_reduced

# Prediction:
def prediction(model, X):
    prediction = model["classifier"].predict_proba(X)
    return prediction

# Model performance:
def model_decision(pred, data=None):
    # Model decision:
    decision = "engaged" if(pred[0][0]>0.5) else "dropping off"
    rounded_prediction = round(pred[0][0]*100, 3)
    # Print result:
    # print("Prediction:")
    return f"Model predicts {rounded_prediction}% of having response rate higher than 30%. [{decision}]"
    if(data):
        print("\nReality:")
        print(f"Actual response rate is {data}.")

# Features Understanding:
def feature_understanding(model, column_names, feature_number, return_all=False):
    pc_summary = pd.DataFrame(data={
        "Features": column_names,
        "PCA1_components": abs(model["pca_8"].components_[0]),
        "PCA2_components": abs(model["pca_8"].components_[1]),
        "PCA3_components": abs(model["pca_8"].components_[2]),
        "PCA4_components": abs(model["pca_8"].components_[3]),
        "PCA5_components": abs(model["pca_8"].components_[4]),
        "PCA6_components": abs(model["pca_8"].components_[5]),
        "PCA7_components": abs(model["pca_8"].components_[6]),
        "PCA8_components": abs(model["pca_8"].components_[7])
    })
    pc_summary = pc_summary.sort_values(by=[f"PCA{feature_number+1}_components"], axis=0, ascending=False)
    imp_features = list(pc_summary.Features)
    if(return_all==True):
        return pc_summary[["Features",f"PCA{feature_number+1}_components"]]
    else:
        return imp_features

# Feature importance plot:
def FI_plot(feature_number, fu_df):
    # fu_df = fu_df.sort_values(by=fu_df.columns[-1], axis=0, ascending=True)
    xdata = fu_df.Features.to_list()
    ydata = fu_df.iloc[:,-1].to_list()

    plt.figure(figsize=(15,5))
    plt.bar(xdata, ydata)
    plt.xticks(rotation=50, ha='right')
    plt.title("Feature importance")
    plt.ylabel("PC values (importance)")

# SHAP plot:
def shap_plot(model, X):
    # SHAP for feature understanding:
    ### Calculate shap values:
    explainer = shap.TreeExplainer(model=model["classifier"])
    shap_values = explainer.shap_values(X=X)
    ### Initialize force_plot:
    shap.initjs()
    shap_plot = shap.force_plot(explainer.expected_value[0], shap_values[0], X, link="logit")
    return shap_plot