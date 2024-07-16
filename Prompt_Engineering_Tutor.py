# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production - Uncomment this line when you deploy

# Cell 2: Title & Description
st.title('Prompt Engineering Tutor Friend:alien::sparkles:')
st.markdown('Hello! I was made to help you answer questions about prompt engineering to test your knowledge AND improve your prompts. This app demonstrates how to use OpenAI GPT-3.5 to answer prompt engineering questions in a deployed envionment.:notepad:Note: An example question has already been entered below for you to try out. Feel free to use that to test the model, or, enter your own question!:woman-raising-hand:Remember, always verify AI-generated responses.')

# Cell 3: Function to analyze text using OpenAI
def analyze_text(text):
  """
  This function sends a text prompt to the OpenAI API using the GPT-3.5 model.

  Arg
      text (str): The prompt engineering question to be answered.

  Returns:
      str: The response generated by the GPT-3.5 model.
  """

  # Ensure your OPENAI_API_KEY is set as an environment variable
  if not api_key:
      st.error("OpenAI API key is not set. Please set it in your environment variables.")
      return

  client = OpenAI(api_key=api_key)
  model = "gpt-3.5-turbo"  # Using the GPT-3.5 model

  # Instructions for the AI (adjust if needed)
  messages = [
      {"role": "system", "content": "You are an assistant who answers technical questions to help improve prompting and prompt engineering skills. When a user enters a question about prompts or provides a prompt, respond in an encouraging way and then provide both the answer to their question and one example of how the user could have written their prompt to improve it. Seperate these two responses into two sections, one that is called ANSWER and one called FEEDBACK. Under ANSWER you will answer whatever the question they asked and under FEEDBACK you will provide an alternate example of how they could have written their prompt or request. If the user only enters a prompt without a question, only provide FEEDBACK. If the user provides both a question and a prompt, provide both an ANSWER and FEEDBACK. If the user makes a statement and has no question, remind the user of your function and provide an example of how they can use your services."},
      {"role": "user", "content": f"Answer the following prompt engineering question:\n{text}"}
  ]

  response = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=0  # Lower temperature for less random responses
  )
  return response.choices[0].message.content

# Cell 4: Streamlit UI
user_input = st.text_area("Enter your question to answer or prompt to improve upon:", "What is one of the most helpful prompt engineering techniques I can use with ChatGPT?")

if st.button('Answer Prompt Engineering Question'):
  with st.spinner('Thinking...:face_in_clouds:'):
      result = analyze_text(user_input)
      st.write(result)
