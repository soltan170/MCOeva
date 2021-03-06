import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn
import time
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

# loading the trained model
pickle_in = open('randomForest.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(lockdown_types, new_cases, statTwoweeksago, r_naught ):   
    
    if lockdown_types == "Malaysia No Lockdown":
        lockdown_types = 0
    elif lockdown_types == "Malaysia MCO":
        lockdown_types = 1
    elif lockdown_types == "Malaysia CMCO":
        lockdown_types = 2
    elif lockdown_types == "Malaysia RMCO":
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
    lockdown_types = st.selectbox('Lockdown Types',("Malaysia MCO","Malaysia CMCO","Malaysia RMCO","Singapore Prelude","Singapore Circuit Breaker","Singapore Phase 1","Singapore Phase 2","Thailand Shutdown","Malaysia No Lockdown","Singapore No Lockdown","Thailand Pre No Lockdown","Thailand Post No Lockdown"))
    new_cases = st.number_input('Today Cases', min_value=0, max_value=5000)
    yesterday_cases = st.number_input('Yesterday Cases', min_value=0, max_value=5000)
    statTwoweeksago = st.number_input('Two Weeks Before Cases', min_value=0, max_value=1500)
    
    if yesterday_cases != 0 :
     r_naught = round(new_cases/yesterday_cases,2)
     
    result =""
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(lockdown_types, new_cases, statTwoweeksago, r_naught)
        if result == "Effective" :
         st.success('Lockdown is {} with R0 {}'.format(result,r_naught))
         if r_naught < 1 :
           currentRate = round(new_cases/statTwoweeksago,2)
           cases = []
           noDays = []
           targetCase = new_cases
           i = 1
           while i < 8 :
            targetCase = round(targetCase*(1-r_naught)**i,0)
            cases.append(targetCase)
            noDaysvar = " +" + str(i) + " Day" 
            noDays.append(noDaysvar)
            i += 1
            
         else :
          currentRate = round(new_cases/statTwoweeksago,2)
          cases = []
          noDays = []
          targetCase = new_cases
          i = 1
          while i < 8 :
           targetCase = round(targetCase*(1-currentRate)**i,0)
           cases.append(targetCase)
           noDaysvar = " +" + str(i) + " Day" 
           noDays.append(noDaysvar)
           i += 1
         
         b = (Bar().add_xaxis(noDays).add_yaxis("",cases).set_global_opts(title_opts=opts.TitleOpts( title="Predicted New Case Number", subtitle="Next few days number of new cases prediction based on R0")))
         st_pyecharts(b)
        else :
         st.error('Lockdown is {} with R0 {}'.format(result,r_naught))
         if r_naught > 1 != 0 :
          cases = []
          noDays = []
          targetCase = new_cases
          i = 1
          while i < 8 :
           targetCase = round(targetCase*(r_naught)**i,0)
           cases.append(targetCase)
           noDaysvar = " +" + str(i) + " Day" 
           noDays.append(noDaysvar)
           i += 1
          
          b = (Bar().add_xaxis(noDays).add_yaxis("",cases).set_global_opts(title_opts=opts.TitleOpts( title="Predicted New Case Number", subtitle="Next few days number of new cases prediction based on R0")))
          st_pyecharts(b)         

     
if __name__=='__main__': 
    main()
