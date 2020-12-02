import sys
import re
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download(['punkt', 'wordnet','stopwords'])

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


def load_data(database_filepath):
    # Load datafrome from database
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table("disaster", con=engine)
    
    # Extract X and Y
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    
    return X, Y, category_names

def tokenize(text):
    # Convert text to lower case:
    text = text.lower()
    
    # Remove punctuation chars:
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    
    # Tokenization:
    tokenized = word_tokenize(text=text)
    
    # Remove stopwords:
    tokenized = [w for w in tokenized if(w not in stopwords.words("english"))]
    
    # Lemmatization:
    tokenized = [WordNetLemmatizer().lemmatize(w) for w in tokenized]
    
    return tokenized


def build_model():
    # Build pipeline
    pipeline = Pipeline(steps=[
        ("vect", CountVectorizer(tokenizer=tokenize)),
        ("tfidf", TfidfTransformer()),
        ("clf", MultiOutputClassifier(AdaBoostClassifier(random_state=42)))
    ])
    
    # GridSearch for finding optimal parameters:
    parameters = {
        'clf__estimator__n_estimators': [50, 100],
        'clf__estimator__learning_rate': [0.01, 0.2]
    }
    cv = GridSearchCV(pipeline, param_grid=parameters, cv=3, n_jobs=-1, verbose=2)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    # Predictions:
    y_pred = model.predict(X_test)
    
    # Classification report:
    for i in range(len(category_names)):
        category = category_names[i]
        print(category)
        print(classification_report(Y_test[category], y_pred[:, i]))


def save_model(model, model_filepath):
    with open(model_filepath, 'wb') as file:  
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()