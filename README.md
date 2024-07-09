## Description
Your Own Answer Engine is a Streamlit-based web application that combines the power of OpenAI's language models with real-time web search capabilities. 
It allows users to ask questions and receive comprehensive answers that are both contextually relevant and up-to-date.

## Features
- User-friendly interface for asking questions
- Integration with OpenAI's GPT-3.5 model for natural language processing ( Can use other LLMs as well)
- Real-time web search functionality using the Tavily API
- Dynamic response generation based on AI analysis and web search results
- Error handling for robust performance

## Prerequisites
- Python 3.7+
- OpenAI API key
- Tavily API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-own-answer-engine.git
   cd your-own-answer-engine
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your question in the text input field and press Enter.

4. Wait for the answer to be generated and displayed.

## How It Works

1. The user enters a question through the Streamlit interface.
2. The question is sent to the OpenAI API, which may decide to perform a web search.
3. If a web search is needed, the Tavily API is queried for relevant information.
4. The search results (if any) are sent back to the OpenAI API for final answer generation.
5. The generated answer is displayed to the user.

## Customization

You can customize the behavior of the Answer Engine by modifying the following:

- Change the OpenAI model by updating the `model` parameter in the `query_openai` function.
- Adjust the number of search results by modifying the `num_results` parameter in the `do_web_search` function.
- Customize the system message in the `answer_with_search` function to change the AI's behavior.
