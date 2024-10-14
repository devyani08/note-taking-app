import streamlit as st
import pandas as pd
from datetime import datetime
import json
import base64

# Initialize session state
if 'pages' not in st.session_state:
    st.session_state.pages = {"root": {}}

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

def create_page(folder_path):
    st.subheader("Create New Page")
    title = st.text_input("Enter page title")
    content = st.text_area("Enter page content")
    if st.button("Save Page"):
        current_folder = st.session_state.pages
        for folder in folder_path:
            current_folder = current_folder[folder]
        current_folder[title] = {
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.success(f"Page '{title}' created successfully in {'/'.join(folder_path)}!")

def view_pages(folder_path):
    st.subheader("View Pages")
    current_folder = st.session_state.pages
    for folder in folder_path:
        current_folder = current_folder[folder]
    
    if not current_folder:
        st.write("No pages or folders in this location.")
    else:
        items = list(current_folder.keys())
        selected_item = st.selectbox("Select a page or folder to view", items)
        if selected_item:
            if isinstance(current_folder[selected_item], dict) and "content" in current_folder[selected_item]:
                st.write(f"## {selected_item}")
                st.write(current_folder[selected_item]["content"])
                st.write(f"Created at: {current_folder[selected_item]['created_at']}")
                
                # Download feature
                page_content = json.dumps(current_folder[selected_item], indent=2)
                st.markdown(get_binary_file_downloader_html(page_content.encode(), f"{selected_item}.json"), unsafe_allow_html=True)
            else:
                st.write(f"Folder: {selected_item}")
                if st.button("Open this folder"):
                    folder_path.append(selected_item)

def create_folder(folder_path):
    st.subheader("Create New Folder")
    folder_name = st.text_input("Enter folder name")
    if st.button("Create Folder"):
        current_folder = st.session_state.pages
        for folder in folder_path:
            current_folder = current_folder[folder]
        current_folder[folder_name] = {}
        st.success(f"Folder '{folder_name}' created successfully in {'/'.join(folder_path)}!")

def main():
    st.set_page_config(page_title="Enhanced Notion Clone", page_icon="📝")
    st.title("Enhanced Notion Clone")
    
    # Initialize folder path
    if 'folder_path' not in st.session_state:
        st.session_state.folder_path = ["root"]
    
    # Display current path
    st.write(f"Current path: /{'/'.join(st.session_state.folder_path[1:])}")
    
    # Option to go back
    if len(st.session_state.folder_path) > 1 and st.button("Go back"):
        st.session_state.folder_path.pop()
        st.experimental_rerun()
    
    menu = ["Create Page", "View Pages", "Create Folder"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Create Page":
        create_page(st.session_state.folder_path)
    elif choice == "View Pages":
        view_pages(st.session_state.folder_path)
    elif choice == "Create Folder":
        create_folder(st.session_state.folder_path)

if __name__ == "__main__":
    main()
