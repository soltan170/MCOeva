import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from pypmml import Model


def predict(LockDownType, CaseNumber, DateRange, SocialDistancing, PeriodEnforce):

    model = Model.fromFile("mcoDT.pmml")
    result = model.predict({
        "lockdown_types" : LockDownType,
        "date_range" : DateRange,
        "social_distancing_rate" : SocialDistancing,
        "cases" : CaseNumber,
        "period_enforce" : PeriodEnforce

    })
    return result

def main():
    # front end elements of the web page
    html_temp = """ 
    <div style ="background-color:cyan;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit MCO effective measure  App</h1> 
    </div> 
    """

    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html=True)

    # following lines create boxes in which user can enter data required to make prediction
    LockDownType = st.selectbox('Lock down Type', ("PKP", "PKPB","PKPP"))
    CaseNumber = st.number_input("number of cases")
    DateRange = st.number_input("number of date enforced")
    SocialDistancing = st.number_input("Social Distance rate")
    PeriodEnforce = st.number_input("Period enforced")


    result = ""

    # when 'Predict' is clicked, make the prediction and store it
    if st.button("Predict"):
        # prediction method calling
        result = predict(LockDownType, CaseNumber, DateRange, SocialDistancing, PeriodEnforce)
        st.success('The MCO status: {}'.format(result))


if __name__=='__main__':
    main()
