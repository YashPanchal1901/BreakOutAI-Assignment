import streamlit as st
import pandas as pd
from langchain import hub
from langchain.agents import AgentExecutor, create_self_ask_with_search_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilyAnswer
import os
from dotenv import load_dotenv
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Load environment variables from the .env file
load_dotenv()

# Access the API keys
gemini_api_key = os.getenv('GEMINI_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

os.environ["GOOGLE_API_KEY"] = gemini_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

# Initialize Tavily search tool and LLM (Google Gemini)
tools = [TavilyAnswer(max_results=1,name="Intermediate Answer")]
prompt = hub.pull("hwchase17/self-ask-with-search")
llm = ChatGoogleGenerativeAI(model="gemini-pro")
agent = create_self_ask_with_search_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)

# Streamlit application setup
st.title("AI Agent Dashboard for Automated Information Retrieval")

# File upload and data handling
st.sidebar.header("Upload or Connect Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")
sheet_url = st.sidebar.text_input("Google Sheet URL")

data = None

# Handle CSV upload
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV Preview:")
    st.write(data.head())

# Handle Google Sheets connection
if sheet_url:
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name("glossy-mason-442016-v5-d89cbc49af47.json", scope)
        client = gspread.authorize(credentials)

        sheet_id = sheet_url.split("/")[5]
        sheet = client.open_by_key(sheet_id).sheet1

        data = pd.DataFrame(sheet.get_all_records())

        st.write("Google Sheets Data Preview:")
        st.write(data.head())
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")

# Select column for processing
if data is not None:
    main_column = st.selectbox("Select Main Column for Entity Search", data.columns)

    # Input custom prompt with placeholder instructions
    st.markdown("""
    
    - Define your prompt using placeholders like `{entity}`.
    
    """)
    custom_prompt = st.text_input("Enter your custom prompt:")
    placeholders = re.findall(r"{(.*?)}", custom_prompt)

    # Start web search and LLM processing
    if st.button("Start Search and Extract Information"):
        results_list = []  # List to store results

        for entity in data[main_column]:

            formatted_prompt = custom_prompt.replace(f"{{{placeholders[0]}}}", str(entity))
            try:
                response = agent_executor.invoke({"input": formatted_prompt})['output']
                results_list.append(response)

            except Exception as e:
                results_list.append(None)  # Append None for errors
                st.error(f"Error processing '{entity}': {e}")

        # Add the results list as a new column to the DataFrame
        data['Extracted Information'] = results_list

        # Display top 5 responses
        st.write("Top 5 Extracted Information:")
        st.write(data.head(5))

        # Download results as CSV
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Extracted Data as CSV", csv, "extracted_data.csv", "text/csv")
