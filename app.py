import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.main import route_query

st.set_page_config(page_title="HungryBot", page_icon="🍜")

st.title("🍜 HungryBot - Bangladesh Food Guide")

with st.form(key="query_form"):
    query = st.text_input("Ask HungryBot about food")
    image = st.file_uploader("Upload menu image", type=["png","jpg","jpeg"])
    submit = st.form_submit_button("Ask")

if submit:
    if not query and image is None:
        st.warning("Please enter a question or upload a menu image.")
    else:
        response = route_query(query, image)
        st.write(response)