import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn


# loading the trained model
pickle_in = open('randomForest.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(lockdown_types, new_cases, statTwoweeksago, r_naught ):   
    
    if lockdown_types == "Malaysia No Lockdown":
        lockdown_types = 0
    elif lockdown_types == "PKP":
        lockdown_types = 1
    elif lockdown_types == "PKPB":
        lockdown_types = 2
    elif lockdown_types == "PKPP":
        lockdown_types = 3
    elif lockdown_types == "Singapore No Lockdown":
        lockdown_types = 4
    elif lockdown_types == "Singapore Prelude":
        lockdown_types = 8
    elif lockdown_types == "Singapore Circuit Breaker":
        lockdown_types = 5
    elif lockdown_types == "Singapore Phase 1":
        lockdown_types = 6
    elif lockdown_types == "Singapore Phase 2":
        lockdown_types = 7
    elif lockdown_types == "Thailand Pre No Lockdown":
        lockdown_types = 10
    elif lockdown_types == "Thailand Shutdown":
        lockdown_types = 11
    else :
        lockdown_types = 9
    # Making predictions 
    prediction = classifier.predict( 
        [[lockdown_types, new_cases, statTwoweeksago, r_naught]])
     
    if prediction == 0:
        pred = 'Not Effective'
    else:
        pred = 'Effective'
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
    lockdown_types = st.selectbox('Lockdown Types',("PKP","PKPB","PKPP","Singapore Prelude","Singapore Circuit Breaker","Singapore Phase 1","Singapore Phase 2","Thailand Shutdown","Malaysia No Lockdown","Singapore No Lockdown","Thailand Pre No Lockdown","Thailand Post No Lockdown"))
    new_cases = st.number_input('Today Cases', min_value=0.00, max_value=20, value=0.02, step=0.01, format=None)
    r_naught = st.number_input('r_naught', float(0), float(15), float(0.20), format="%.2f")
    statTwoweeksago = st.number_input('Two Weeks Before Cases', min_value=0, max_value=1500)
   
    
    result =""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(lockdown_types, new_cases, statTwoweeksago, r_naught)
        st.success('Lockdown is {} '.format(result))
        
        
     
if __name__=='__main__': 
    main()
