#!/usr/bin/env python

# AI/ML imports
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# API imports
from fastapi import FastAPI

# Standard library imports
import csv

app = FastAPI()

# Helpers
def _prep_data(df, target):
    # Split up data into features and targets
    print("Splitting data...")
    y = df[target]
    x = df.drop([target], axis=1)

    return train_test_split(x, y, test_size=0.33, random_state=42)

def _decision_tree_trainer(df, target):
    x_train, x_test, y_train, y_test = _prep_data(df, target)
    print("Creating classifier...")
    clf = DecisionTreeClassifier(random_state=0)

    # Train the classifier
    print("Training decision tree...")
    trained_clf = clf.fit(x_train, y_train)

    # Get accuracy for train and test sets
    print("Calculating accuracy...")
    train_accuracy = clf.score(x_train, y_train)
    test_accuracy = clf.score(x_test, y_test)

    return train_accuracy, test_accuracy

# Start container function
@app.get("/train")
async def start_container():
    df = pd.read_csv('test.csv')
    train_accuracy, test_accuracy = _decision_tree_trainer(df, 'variety')
    return train_accuracy, test_accuracy