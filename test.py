import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn


# loading the trained model
pickle_in = open('myClassifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(lockdown_types, new_cases, total_case, date_range, r_naught ):   
 
    
    
    if lockdown_types == "PKP":
        lockdown_types = 0
        location = 0
    elif lockdown_types == "PKPB":
        lockdown_types = 1
        location = 0
    elif lockdown_types == "PKPP":
        lockdown_types = 2
        location = 0
    elif lockdown_types == "SingaporePrelude":
        lockdown_types = 3
        location = 1
    elif lockdown_types == "SingaporeCB":
        lockdown_types = 4
        location = 1
    elif lockdown_types == "SingaporePhase1":
        lockdown_types = 5
        location = 1
    elif lockdown_types == "SingaporePhase2":
        lockdown_types = 5
        location = 1
    elif lockdown_types == "SingaporePhase3":
        lockdown_types = 5
        location = 1
    else :
        lockdown_types = 6
        location = 2
    # Making predictions 
    prediction = classifier.predict( 
        [[location, new_cases, total_case, lockdown_types, date_range, r_naught]])
     
    if prediction == 0:
        pred = 'Effective'
    else:
        pred = 'Not Effective'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:gray;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Lockdown Effectiveness Prediction ML App</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    lockdown_types = st.selectbox('Lockdown Types',("PKP","PKPB","PKPP","SingaporePrelude","SingaporeCB","SingaporePhase1","SingaporePhase2"))
    new_cases = st.number_input('Today Cases', min_value=0, max_value=1500)
    previous_case = st.number_input('Previous Day Cases', min_value=0, max_value=1500)
    total_case = st.number_input('Total Cases', min_value=0)
    date_range = st.slider('Date Range', min_value=0, max_value=365)
    
    if previous_case == 0 :
        r_naught = 0
    else :
        r_naught = round(new_cases/previous_case,2)
    
    result =""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(lockdown_types, new_cases, total_case, date_range, r_naught)
        st.success('Lockdown is {}'.format(result))
        
     
if __name__=='__main__': 
    main()
