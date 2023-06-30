import streamlit as st
import openai
from steamship import Steamship
from streamlit_player import st_player
import json

st.set_page_config(page_title="Ask WardleyGPT")
st.title("Ask WardleyGPT Anything")
st.sidebar.markdown("# Using AI, ask anything about Wardley Mapping")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.2.0")
st.sidebar.divider()
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.markdown("Wardley Mapping Community Content")
st.sidebar.markdown("1M+ Vectors")

# Load the package instance stub only if it has not been loaded before
#if "pkg" not in st.session_state:
#    # Load the package instance stub.
#    st.session_state.pkg = Steamship.use(
#        "wardleybok",
#        instance_handle="wardleybok-beg",
#        api_key = st.secrets["STEAMSHIP_API_KEY"]
#    )

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

#if prompt:
#    with st.spinner("Generating response..."):
#        # Invoke the method
#        response = st.session_state.pkg.invoke(
#            "qa",
#            query=prompt
#        )#
#
#        # Parse the JSON response
#        response_json = json.loads(response)#####
#
#        # Display answer
#        answer = response_json["answer"]
#        st.write(f"**Answer:** {answer}")#
#
#        st.write("Content from Wardley Community")
#        for i in range(len(response_json['source_urls'])):
#            source_title = response_json.get('source_title', [''])[i].lower()
#            source_container = st.container()
#            with source_container:
#                st.write(f"Source {i+1}:")
#                if 'source_urls' in response_json and len(response_json['source_urls']) > i:
#                    video_id = "https://www.youtube.com/watch?feature=share&v=" + response_json['source_urls'][i]
#                    key = f"video_{i}"
#                    st_player(video_id, height=150, key=key)
#                    st.write("")
