import streamlit as st
from openai import OpenAI
import os
import json

# ... (previous code remains the same)

# Add this function to extract conversation history
def extract_conversation():
    conversation = st.session_state.conversation_history
    return json.dumps(conversation, indent=2)

# Modify the Streamlit UI section
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
    conversation_json = extract_conversation()
    st.download_button(
        label="Download Conversation",
        data=conversation_json,
        file_name="conversation_history.json",
        mime="application/json"
    )

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    st.text(f"{message['role'].capitalize()}: {message['content']}")
