import pandas as pd
import numpy as np
import math
import streamlit as st

def entropy(dataset):
    sys_entropy = 0
    freq = dict()
    for i in dataset['disease']:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
        for keys in freq.keys():
            prob1 = freq[keys] / len(dataset['disease'])
            prob2 = 1 - prob1
            if prob1 != 1:
                sys_entropy += -(prob1 * math.log(prob1, 2)) - (prob2 * math.log(prob2, 2))
            else:
                sys_entropy = 0
    return sys_entropy

def freq(diseases):
    rt = dict()
    for i in diseases['disease']:
        if i in rt.keys():
            rt[i] += 1
        else:
            rt[i] = 1
    maxi = max(rt, key=lambda x: rt[x])
    return maxi

df = pd.read_csv("dataset.csv")
df2 = pd.read_csv('symptom_Description.csv')
df3 = pd.read_csv('symptom_precaution.csv')

s = []

for i in range(len(df['Disease'])):
    temp = []
    for j in range(1, 18):
        symp = 'Symptom_' + str(j)
        if pd.isnull(df[symp][i]):
            break
        temp.append(df[symp][i].replace(' ', ''))
    s.extend(temp)
s = list(set(s))
s.append("disease")

new_df = pd.DataFrame(0, index=np.arange(len(df['Disease'])), columns=s)

for i in range(len(df['Disease'])):
    for j in range(1, 18):
        symp = 'Symptom_' + str(j)
        if pd.isnull(df[symp][i]):
            break
        new_df.at[i, df[symp][i].replace(" ", "")] = 1

new_df['disease'] = df['Disease'].tolist()

infections = [x.lower() for x in st.text_input('Type your symptoms', ' ').split(' ')]
t = st.button("click here")
infections = [i for i in infections if i in new_df.columns]
if 'disease' in s:
    s.remove('disease')

test = pd.DataFrame(0, index=[0], columns=s)

def pred(infect, sympt, columns, dtset):
    for i in infect:
        if i in columns:
            sympt[i][0] = 1
    output = dtset  # Replace with your tree logic
    st.write(freq(output))
    return freq(output)

if t:
    result = pred(infections, test, s, new_df)

    if result in df2['Disease'].tolist():
        st.write(df2['Description'][df2['Disease'].tolist().index(result)])

    if result in df3['Disease'].tolist():
        st.write("Precautions:")
        st.write(df3['Precaution_1'][df3['Disease'].tolist().index(result)])
        st.write(df3['Precaution_2'][df3['Disease'].tolist().index(result)])
        st.write(df3['Precaution_3'][df3['Disease'].tolist().index(result)])
