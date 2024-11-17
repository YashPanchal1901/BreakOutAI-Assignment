# AI Agent Dashboard for Automated Information Retrieval

## Project Description
This project is an AI-powered dashboard that allows users to upload CSV files or connect to a Google Sheet for data processing. The application performs automated web searches for entities specified in the dataset and extracts relevant information using an LLM (Google Gemini) integrated with LangChain's Tavily Search. The results are displayed in a structured format and can be downloaded as a CSV file.

## Setup Instructions
Follow these steps to set up and run the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-agent-dashboard.git
   cd ai-agent-dashboard
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.8+ installed. Run the following command to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create and Download `credentials.json`**:
   To access Google Sheets securely, you need a `credentials.json` file:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create or select an existing project.
   - Enable the **Google Sheets API** and **Google Drive API**.
   - Navigate to **APIs & Services > Credentials** and click **Create Credentials > Service Account**.
   - Fill in the required details, create the service account, and go to the **Keys** tab.
   - Click **Add Key > Create new key**, choose **JSON** format, and download the `credentials.json` file.
   - Place this file in the root directory of your project.

4. **Share Your Google Sheet**:
   - Open your Google Sheet and click **Share**.
   - Share the sheet with the service account email found in your `credentials.json` file (usually ends with `@<project-name>.iam.gserviceaccount.com`).

5. **Set Up Environment Variables**:
   Create a `.env` file in the root directory with the following content:
   ```dotenv
   GEMINI_API_KEY=your_google_gemini_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Replace `your_google_gemini_api_key` and `your_tavily_api_key` with your actual API keys.

6. **Run the Application**:
   Start the Streamlit app using:
   ```bash
   streamlit run app.py
   ```

## Usage Guide
1. **Upload a CSV File**:
   - Navigate to the sidebar and click the "Browse" button to upload a CSV file.
   - The application will display a preview of the uploaded data.

2. **Connect to a Google Sheet**:
   - Enter the URL of the Google Sheet in the provided text box.
   - Ensure that the Google Sheet is shared with the service account email from `credentials.json`.

3. **Select the Main Column**:
   - Choose the primary column from the uploaded data for the entity search.

4. **Define a Custom Query**:
   - Input your custom query in the text box, using placeholders like `{entity}` to be dynamically replaced by each entity in the selected column.

5. **Extract Information**:
   - Click the "Start Search and Extract Information" button to initiate the web search and LLM processing.
   - The extracted data will be displayed and can be downloaded as a CSV file.

## API Keys and Environment Variables
### Required API Keys:
- **Google Gemini API Key**: Used to integrate with the Google Gemini LLM.
- **Tavily API Key**: Used for performing web searches through LangChain's Tavily Search tool.

### Environment Setup:
Ensure that your `.env` file contains the following:
```dotenv
GEMINI_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```
These keys will be automatically loaded by the `dotenv` package in your Python script.

## Optional Features
- **Dynamic Prompt Formatting**: Users can specify custom prompts with placeholders like `{entity}`.
- **Google Sheets Integration**: Connects directly to a Google Sheet and reads data securely.
- **Error Handling**: Gracefully handles failed API calls and displays informative error messages.
- **Download Extracted Data**: Provides a button to download the final DataFrame as a CSV file.

## Notes
- Ensure that your `credentials.json` file is kept secure and not committed to version control. Add it to your `.gitignore` file.
- Use a virtual environment or `venv` to manage dependencies.

For more information and detailed setup, please refer to the [Google Cloud Documentation](https://cloud.google.com/docs) and [Streamlit Documentation](https://docs.streamlit.io/).
