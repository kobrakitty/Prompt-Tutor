import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Used in production - Uncomment this line when you deploy

# Title & Description
st.title('Prompt Engineering Friend:alien:')
st.markdown('Hello! I was made to answer questions about prompt engineering and improve your prompts. One example has already been entered into the field below for you to try out. You can use the pre-entered example to test the model first (just click SUBMIT! below) OR enter your own question (much more fun!!). :woman-raising-hand: Remember, always verify AI-generated responses.')

# Function to analyze text using OpenAI
def analyze_text(text, conversation_history):
    """
    This function sends a text prompt to the OpenAI API using the GPT-3.5 model.
    Args:
        text (str): The prompt engineering question to be answered.
        conversation_history (list): List of previous messages in the conversation.
    Returns:
        str: The response generated by the GPT-3.5 model.
    """
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return

    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"  # Using the GPT-3.5 model

    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are an assistant who answers questions to help improve prompting and prompt engineering skills. When a user enters a question about prompts or provides a prompt, respond in an encouraging way and then provide both the answer to their question and one example of how the user could have written their prompt to improve it. Separate these two responses into two sections, one that is called ANSWER and one called FEEDBACK. Under ANSWER you will answer whatever the question they asked and under FEEDBACK you will provide an alternate example of how they could have written their prompt or request. If the user only enters a prompt without a question, only provide FEEDBACK. If the user provides both a question and a prompt, provide both an ANSWER and FEEDBACK. If the user makes a statement and has no question, remind the user of your function and provide an example of how they can use your services."}
    ]
    
    # Add conversation history to messages
    messages.extend(conversation_history)
    
    # Add the current user message
    messages.append({"role": "user", "content": f"Answer the following prompt engineering question:\n{text}"})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0  # Lower temperature for less random responses
    )
    return response.choices[0].message.content

# Function to extract conversation history as text
def extract_conversation():
    conversation = st.session_state.conversation_history
    text_content = ""
    for message in conversation:
        text_content += f"{message['role'].capitalize()}: {message['content']}\n\n"
    return text_content

# Streamlit UI
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

user_input = st.text_area("Enter your question or the prompt you want to improve:", "What is one of the most helpful prompt engineering techniques I can use with ChatGPT?")

col1, col2 = st.columns(2)

if col1.button('SUBMIT! :sun_with_face: '):
    with st.spinner('Thinking...:face_in_clouds:'):
        result = analyze_text(user_input, st.session_state.conversation_history)
        st.write(result)
        
        # Update conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        st.session_state.conversation_history.append({"role": "assistant", "content": result})

if col2.button('Extract Conversation'):
    conversation_text = extract_conversation()
    st.download_button(
        label="Download Conversation",
        data=conversation_text,
        file_name="conversation_history.txt",
        mime="text/plain"
    )

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    st.text(f"{message['role'].capitalize()}: {message['content']}")
