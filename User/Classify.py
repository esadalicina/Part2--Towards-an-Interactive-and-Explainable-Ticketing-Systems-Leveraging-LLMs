import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt
import streamlit as st


# Load the model and required objects with error handling

@st.cache_resource
def load_model():
    #loaded_model = joblib.load('/mount/src/ticketing-system/Model/TF/modelML.pkl')
    #tfidf_vectorizer = joblib.load('/mount/src/ticketing-system/Model/TF/tfidf_transformer.pkl')
    loaded_model = joblib.load('/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Model/TF/modelML.pkl')
    tfidf_vectorizer = joblib.load('/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Model/TF/tfidf_transformer.pkl')

    return loaded_model, tfidf_vectorizer

loaded_model, tfidf_vectorizer = load_model()

# Classify the new tickets
def predict_lr(text):
    Topic_names = {
        0: 'Credit Reporting and Debt Collection',
        1: 'Credit Cards and Prepaid Cards',
        2: 'Bank Account or Service',
        3: 'Loans',
        4: 'Money Transfers and Financial Services'
    }
    X_new_tfidf = tfidf_vectorizer.transform(text)
    predicted = loaded_model.predict(X_new_tfidf)
    predicted_proba = loaded_model.predict_proba(X_new_tfidf)
    return Topic_names[predicted[0]], predicted[0], predicted_proba

# Function to explain predictions using KernelExplainer
def explain_texts(texts):
    X_tfidf = tfidf_vectorizer.transform(texts)
    background = np.zeros(X_tfidf.shape)  # Using a background dataset of zeros
    explainer = shap.KernelExplainer(loaded_model.predict_proba, background)
    shap_values = explainer.shap_values(X_tfidf)
    return shap_values

# Simplified SHAP explanation plot
def plot_shap_values(texts, class_index=0):
    shap_values = explain_texts(texts)

    # Extract shap_values for the specified class
    shap_values_class = shap_values[0][:, class_index]

    # Filter SHAP values to include only those greater than 0
    positive_mask = shap_values_class > 0
    positive_shap_values = shap_values_class[positive_mask].reshape(1, -1)
    positive_feature_names = tfidf_vectorizer.get_feature_names_out()[positive_mask]

    plt.figure(figsize=(10, 5))
    plt.title(f'Words Impact on Classification')

    shap.summary_plot(positive_shap_values, feature_names=positive_feature_names)
    plt.gcf().patch.set_linewidth(2)
    plt.gcf().patch.set_edgecolor('black')
    st.pyplot(plt)
