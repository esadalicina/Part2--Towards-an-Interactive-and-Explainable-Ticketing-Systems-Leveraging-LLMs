import joblib

# Load the model
loaded_model = joblib.load('/Users/esada/Desktop/pythonProject/Model/TF/modelML.pkl')
# Load the objects
vect = joblib.load('/Users/esada/Desktop/pythonProject/Model/TF/count_vect.pkl')
transformer = joblib.load('/Users/esada/Desktop/pythonProject/Model/TF/tfidf_transformer.pkl')


# Classify the new tickets
def predict_lr(text):
    Topic_names = {0: 'Credit Reporting and Debt Collection', 1: 'Credit Cards and Prepaid Cards',
                   2: 'Bank Account or Service', 3: 'Loans', 4: 'Money Transfers and Financial Services'}
    X_new_counts = vect.transform(text)
    X_new_tfidf = transformer.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    return Topic_names[predicted[0]]
