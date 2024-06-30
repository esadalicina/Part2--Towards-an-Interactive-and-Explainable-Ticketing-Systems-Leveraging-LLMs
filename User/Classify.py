import joblib
import shap
import pandas as pd

# Load the model
loaded_model = joblib.load('/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Model/TF/modelML.pkl')
# Load the objects
vect = joblib.load('/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Model/TF/count_vect.pkl')
transformer = joblib.load('/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Model/TF/tfidf_transformer.pkl')

# Classify the new tickets
def predict_lr(text):
    Topic_names = {0: 'Credit Reporting and Debt Collection', 1: 'Credit Cards and Prepaid Cards',
                   2: 'Bank Account or Service', 3: 'Loans', 4: 'Money Transfers and Financial Services'}
    X_new_counts = vect.transform(text)
    X_new_tfidf = transformer.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    predicted_proba = loaded_model.predict_proba(X_new_tfidf)
    return Topic_names[predicted[0]], predicted[0], predicted_proba

# Function to explain predictions
def explain_prediction(text):
    pass


# Example usage
text = ["I am having trouble logging into my bank account. I have tried multiple times and "
        "I have received no response. I tried resetting my password, but that did not seem to work either. "
        "I am concerned that there may be an issue with my account security or that someone "
        "has accessed my account without my permission."]

prediction, label, prob = predict_lr(text)
print(f"Prediction: {prediction}")
print(f"Predicted class index: {label}")
print(f"Prediction probabilities: {prob}")
# Explain the prediction
explain_prediction(text)
