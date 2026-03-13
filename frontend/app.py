import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.main import route_query

st.set_page_config(page_title="HungryBot", page_icon="🍜")

st.title("🍜 HungryBot - Bangladesh Food Guide")

st.write("Ask about Bangladeshi foods (e.g., 'Tell me about Mezban Beef') or ask 'Where is ...' to get location links.")

with st.form(key="query_form"):
    query = st.text_input("Ask HungryBot about food")

    image = st.file_uploader("Upload menu image", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Ask")


if submitted:
    response = route_query(query, image)
    st.write(response)
