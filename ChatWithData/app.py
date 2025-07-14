import os
import streamlit as st
import tempfile
import json
import requests
import pandas as pd
import pandasai as pai
import google.generativeai as genai
from typing import Optional, Any
from pandasai.dataframe.base import DataFrame
from pandasai.data_loader.semantic_layer_schema import SemanticLayerSchema, Source, Column
from pandasai.core.response.chart import ChartResponse
from pandasai.core.response.dataframe import DataFrameResponse
from pandasai.core.response.number import NumberResponse
from pandasai.core.response.string import StringResponse
from pandasai.dataframe.base import DataFrame
from pandasai.llm.base import LLM
from pandasai.agent.base import Agent
import requests
from pandasai.llm.base import LLM
from typing import Optional

class GeminiLLM(LLM):
    def __init__(self, api_key: str, model="gemini-2.5-pro"):
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    @property
    def type(self) -> str:
        return "gemini"

    def call(self, instruction: str, context: dict) -> str:
        response = self.client.generate_content(str(instruction))
        return response.text if hasattr(response, 'text') else str(response)

        
st.title("Chat with Data")
if 'csv' not in st.session_state:
    st.session_state.csv = False
if 'description' not in st.session_state:
    st.session_state.description = False
if 'json' not in st.session_state:
    st.session_state.json = False
if 'path' not in st.session_state:
    st.session_state.path = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'schema' not in st.session_state:
    st.session_state.schema = None
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'description_text' not in st.session_state:
    st.session_state.description_text = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if not st.session_state.csv or not st.session_state.description or not st.session_state.json:
    file = st.file_uploader("Upload your data as CSV format",type=["csv"])
    if file:
        st.session_state.csv = True
        st.session_state.df = pd.read_csv(file)
        st.session_state.path = file.name
    description = st.text_input("Enter a description of your data:")
    if description:
        st.session_state.description_text = description
        st.session_state.description = True

    metadata = st.file_uploader("Upload your columns metadata as JSON format", key="f2",type=["json"])
    if metadata:
        st.session_state.json = True
        columns = json.load(metadata)
        st.session_state.schema = SemanticLayerSchema(name="schema",description=st.session_state.description_text,columns=columns,source=Source(type="csv",path=st.session_state.path))

if st.session_state.csv and st.session_state.description and st.session_state.json:
    llm = GeminiLLM(api_key=st.secrets["GOOGLE_API_KEY"])
    df = DataFrame(data=st.session_state.df, schema=st.session_state.schema)
    st.session_state.agent = Agent(dfs=df, config={"llm": llm})
    st.session_state.csv = True
    st.session_state.description = True
    st.session_state.json = True
    chat_container = st.container()
    question = st.text_input("Ask a question about the data:", key="q", label_visibility="collapsed", placeholder="Type your question here...")
    
    if question:
        try:
            response = None
            if len(st.session_state.conversation) == 0:
                response = st.session_state.agent.chat(question) 
            else:
                response = st.session_state.agent.follow_up(question)
            
            st.session_state.conversation.append({"role": "user", "type": "text", "message": question})
            if isinstance(response, DataFrameResponse):
                response = response.value
                st.session_state.conversation.append({"role": "bot", "type": "dataframe", "message": response})
            elif isinstance(response, ChartResponse):
                st.session_state.conversation.append({"role": "bot", "type": "chart", "message": response})
            elif isinstance(response, (NumberResponse, StringResponse)):
                st.session_state.conversation.append({"role": "bot", "type": "text", "message": str(response)})
            else:
                st.session_state.conversation.append({"role": "bot", "type": "text", "message": "Unsupported response type: "+str(response.type)})
        except Exception as e:
            st.session_state.conversation.append({"role": "user", "type": "text", "message": question})
            st.session_state.conversation.append({"role": "bot", "type": "text", "message": "Invalid Question"})
            print(st.session_state.conversation)
            print(e)
        with chat_container:
            st.markdown("<div style='height: 80vh; overflow-y: auto;'>", unsafe_allow_html=True)
    
            for chat in st.session_state.conversation:
                if chat["role"] == "user":
                    st.markdown(
            f"""
            <div style='text-align: right; margin-bottom: 10px;'>
                <div style='display: inline-block; background-color: #dcf8c6; padding: 10px; border-radius: 10px; max-width: 70%;'>
                    {chat["message"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
                    )

                elif chat["role"] == "bot":
                    if chat["type"] == "text":
                        st.markdown(
                f"""
                <div style='text-align: left; margin-bottom: 10px;'>
                    <div style='display: inline-block; background-color: #f1f0f0; padding: 10px; border-radius: 10px; max-width: 70%;'>
                        {chat["message"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
                        )

                    elif chat["type"] == "dataframe":
                        st.markdown(
                f"""
                <div style='text-align: left; margin-bottom: 10px;'>
                    <div style='background-color: #f1f0f0; padding: 10px; border-radius: 10px; max-width: 90%;'>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
                        )
                        st.dataframe(chat["message"])

                    elif chat["type"] == "chart":
                        st.markdown(
                f"""
                <div style='text-align: left; margin-bottom: 10px;'>
                    <div style='background-color: #f1f0f0; padding: 10px; border-radius: 10px; max-width: 90%;'>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
                        )
                        st.image(chat["message"]._get_image()) 
