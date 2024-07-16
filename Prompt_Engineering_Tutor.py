# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production - Uncomment this line when you deploy

# Cell 2: Title & Description
st.title(':spiral_note_pad:Prompt Engineering Interview Assistant:spiral_note_pad:')
st.markdown('I was made to help you answer questions about prompt engineering to test your knowledge and improve your prompts. This app demonstrates how to use OpenAI GPT-3.5 to answer prompt engineering questions in a deployed envionment. Remember, always verify AI-generated responses.')

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
      {"role": "system", "content": "You are an assistant who answers technical questions to help improve prompting and prompt engineering skills. When a user enters a question about prompts or provides a prompt, respond in an encouraging way and then provide both the answer to their question and one example of how the user could have written their prompt to improve it. Seperate these two responses into two sections, one that is called ANSWER and one called FEEDBACK. Under ANSWER you will answer whatever the question they asked and under FEEDBACK you will provide an alternate example of how they could have written their prompt or request."},
      {"role": "user", "content": f"Answer the following prompt engineering question:\n{text}"}
  ]

  response = client.chat.completions.create(
      model=model,
      messages=messages,
      temperature=0  # Lower temperature for less random responses
  )
  return response.choices[0].message.content

# Cell 4: Streamlit UI
user_input = st.text_area("Enter question to answer:", "What is one of the easiest prompt engineering technique to practice every time I use ChatGPT to get a helpful response? Tell me the name of it and give me an example.")

if st.button('Answer Prompt Engineering Question'):
  with st.spinner(':face_in_clouds:Thinking...:face_in_clouds:'):
      result = analyze_text(user_input)
      st.write(result)