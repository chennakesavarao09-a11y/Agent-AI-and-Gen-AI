# Implemeted a simple dashboard in meet 

import streamlit as st 
import pandas as pd 

st.set_page_config(page_title="Student Dahboard", layout="wide")

#title..
st.title("Performance Dashboard")
st.write("Welcome to Dashboard")

#sidebar for chosing pages...
st.sidebar.title("Navigation")

option=st.sidebar.selectbox(
    "select page",
    ["Dashboard","About"]
)

if option=="Dashboard":
    data={
        "students":["A","B","C","D"],
        "marks":[67,43,89,25]
    }
    df=pd.DataFrame(data)
    
    #dashboard metrics...
    c1,c2,c3=st.columns(3)
    
    c1.metric("Total students", len(df))
    c2.metric("Average", round(df["marks"].mean(),2))
    c3.metric("hig score", df["marks"].max())

    st.divider()
    
    #chart...
    st.subheader("student marks")
    st.bar_chart(df, use_container_width=True)
    
    st.subheader("student details")
    st.dataframe(df, use_container_width=True)
    
elif option=="About":
    st.header("about dashboard")
    st.write("Welcome to dashboard")