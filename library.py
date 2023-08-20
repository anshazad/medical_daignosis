import pandas as pd
import streamlit as st
from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np

# Loading dataset
data = pd.read_csv("dataset.csv")
desc_data = pd.read_csv('symptom_Description.csv')
precaution_data = pd.read_csv('symptom_precaution.csv')

# Extracting unique symptoms
symptoms = set()
for i in range(len(data)):
    for j in range(1, 18):
        symptom_col = 'Symptom_' + str(j)
        if pd.notnull(data[symptom_col][i]):
            symptoms.add(data[symptom_col][i].replace(" ", ""))
symptoms = list(symptoms)
symptoms.append("disease")

# Creating new dataset with symptom columns
new_df = pd.DataFrame(0, index=np.arange(len(data)), columns=symptoms)

# Populating new dataset with symptom values
for i in range(len(data)):
    for j in range(1, 18):
        symptom_col = 'Symptom_' + str(j)
        if pd.notnull(data[symptom_col][i]):
            new_df.at[i, data[symptom_col][i].replace(" ", "")] = 1
new_df['disease'] = data['Disease'].tolist()

# Creating input dataset and labels
inputs = new_df.drop('disease', axis='columns')
target = new_df['disease']

# Splitting data for training and testing
x_train, x_test, y_train, y_test = train_test_split(inputs, target, test_size=0.2)
model = tree.DecisionTreeClassifier()
model.fit(x_train, y_train)

# Interface and prediction
count = 0
infections = []
t = st.button("Click here")
infections = [x.lower() for x in st.text_input('Enter your symptoms', ' ').split(' ')]

if 'disease' in symptoms:
    symptoms.remove('disease')

test = pd.DataFrame(0, index=[0], columns=symptoms)

def predict_disease(infect, sympt, cols):
    for i in infect:
        if i in cols:
            sympt[i][0] = 1
    st.write(model.predict(sympt))
    return model.predict(sympt)

if t:
    result = predict_disease(infections, test, symptoms)
    if result in desc_data['Disease'].tolist():
        st.write(desc_data['Description'][desc_data['Disease'].tolist().index(result)])
    if result in precaution_data['Disease'].tolist():
        st.write("Precautions:")
        st.write(precaution_data['Precaution_1'][precaution_data['Disease'].tolist().index(result)])
        st.write(precaution_data['Precaution_2'][precaution_data['Disease'].tolist().index(result)])
        st.write(precaution_data['Precaution_3'][precaution_data['Disease'].tolist().index(result)])
