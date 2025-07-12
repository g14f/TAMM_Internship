import os
import streamlit as st
import tempfile
import json
import pandas as pd
import pandasai as pai
from pandasai.data_loader.semantic_layer_schema import SemanticLayerSchema, Source
from pandasai.core.response.chart import ChartResponse
from pandasai.core.response.dataframe import DataFrameResponse
from pandasai.core.response.number import NumberResponse
from pandasai.core.response.string import StringResponse
from pandasai.smart_dataframe import SmartDataframe
from pandasai.llm.base import LLM
from pandasai.pandas_ai import PandasAI
import google.generativeai as genai

class GeminiLLM(LLM):
    def __init__(self, api_key: str, model="gemini-2.5-pro"):
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def call(self, prompt: str, **kwargs) -> str:
        response = self.client.generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)

pai_api_key = st.secrets["PAI_API_KEY"]
google_api_key = st.secrets["GOOGLE_API_KEY"]
pai.api_key.set(pai_api_key)

st.title("Chatbot")
df = None

if 'csv' not in st.session_state:
    st.session_state.csv = False
if 'description' not in st.session_state:
    st.session_state.description = False
if 'json' not in st.session_state:
    st.session_state.json = False
if 'df' not in st.session_state:
    st.session_state.schema = None
if 'path' not in st.session_state:
    st.session_state.path = None
if 'columns' not in st.session_state:
    st.session_state.columns = None
if 'description_text' not in st.session_state:
    st.session_state.description_text = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'pandas_ai' not in st.session_state:
    st.session_state.pandas_ai = None

if not st.session_state.csv or not st.session_state.description or not st.session_state.json:
    file = st.file_uploader("Upload your data as CSV format")
    if file:
        st.session_state.csv = True
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(file.read())
            st.session_state.path = tmp.name

    description = st.text_input("Enter a description of your data:")
    if description:
        st.session_state.description_text = description
        st.session_state.description = True

    metadata = st.file_uploader("Upload your columns metadata as JSON format", key="f2")
    if metadata:
        st.session_state.json = True
        st.session_state.columns = json.load(metadata)

if st.session_state.csv and st.session_state.description and st.session_state.json and st.session_state.path and st.session_state.description_text and st.session_state.columns:
    if st.session_state.df is None:
        llm = GeminiLLM(api_key=google_api_key)
        for col in st.session_state.columns:
            col["name"] = str(col["name"])
        source = Source(type="csv", path=st.session_state.path)
        st.session_state.schema = SemanticLayerSchema(name="schema1", description=st.session_state.description_text, columns=st.session_state.columns, source=source,dataframe=df)
        st.session_state.pandas_ai = PandasAI(llm=llm, verbose=True)

    st.session_state.csv = True
    st.session_state.description = True
    st.session_state.json = True

    chat_container = st.container()
    question = st.text_input("Ask a question about the data:", key="q", label_visibility="collapsed", placeholder="Type your question here...")
    
    if question:
        try:
            response = None
            if len(st.session_state.conversation) == 0:
                response = st.session_state.pandas_ai.chat([st.session_state.schema],question) 
            else:
                response = st.session_state.pandas_ai.follow_up([st.session_state.schema],question)
            
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
            st.write(e.__traceback__str__())
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
