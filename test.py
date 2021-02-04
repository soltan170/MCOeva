import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn
import time

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
    <div style ="background-color:rgba(111, 66, 193, 0.05);padding:15px"> 
    <h1 style ="color:#824b4b;text-align:center;">Lockdown Effectiveness Prediction</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
    
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://raw.githubusercontent.com/Ashish-Arya-CS/CovDetec/main/abcd1.png");
    background-size: cover;
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # following lines create boxes in which user can enter data required to make prediction 
    lockdown_types = st.selectbox('Lockdown Types',("PKP","PKPB","PKPP","Singapore Prelude","Singapore Circuit Breaker","Singapore Phase 1","Singapore Phase 2","Thailand Shutdown","Malaysia No Lockdown","Singapore No Lockdown","Thailand Pre No Lockdown","Thailand Post No Lockdown"))
    new_cases = st.number_input('Today Cases', min_value=0, max_value=1500)
    statTwoweeksago = st.number_input('Two Weeks Before Cases', min_value=0, max_value=1500)
    r_naught = st.number_input('r_naught', min_value=0.00, max_value=20.0, value=0.02, step=0.01, format="%.2f")
   
    
    result =""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(lockdown_types, new_cases, statTwoweeksago, r_naught)
        st.success('Lockdown is {} '.format(result))
        # Get some data.
        data = np.random.randn(10, 2)

        # Show the data as a chart.
        chart = st.line_chart(data)

        # Wait 1 second, so the change is clearer.
        time.sleep(1)

        # Grab some more data.
        data2 = np.random.randn(10, 2)

        # Append the new data to the existing chart.
        chart.add_rows(data2)
        
 
     
if __name__=='__main__': 
    main()
