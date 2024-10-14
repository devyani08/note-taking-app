import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if 'pages' not in st.session_state:
    st.session_state.pages = {}

def create_page():
    title = st.text_input("Enter page title")
    content = st.text_area("Enter page content")
    if st.button("Save Page"):
        st.session_state.pages[title] = {
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success(f"Page '{title}' created successfully!")

def view_pages():
    if not st.session_state.pages:
        st.write("No pages created yet.")
    else:
        page_titles = list(st.session_state.pages.keys())
        selected_page = st.selectbox("Select a page to view", page_titles)
        if selected_page:
            st.write(f"## {selected_page}")
            st.write(st.session_state.pages[selected_page]["content"])
            st.write(f"Created at: {st.session_state.pages[selected_page]['created_at']}")

def main():
    st.set_page_config(page_title="Notion Clone", page_icon="📝")
    st.title("Notion Clone")
    
    menu = ["Create Page", "View Pages"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create Page":
        create_page()
    elif choice == "View Pages":
        view_pages()

if __name__ == "__main__":
    main()
