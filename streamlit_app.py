import streamlit as st
import json
import base64
from datetime import datetime

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = {"folders": {}, "pages": {}}

def get_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'

def create_folder():
    st.subheader("Create New Folder")
    folder_name = st.text_input("Enter folder name")
    if st.button("Create Folder"):
        if folder_name not in st.session_state.data["folders"]:
            st.session_state.data["folders"][folder_name] = []
            st.success(f"Folder '{folder_name}' created successfully!")
        else:
            st.error(f"Folder '{folder_name}' already exists!")

def create_page():
    st.subheader("Create New Page")
    folder_options = [""] + list(st.session_state.data["folders"].keys())
    folder = st.selectbox("Select folder (optional)", folder_options)
    title = st.text_input("Enter page title")
    content = st.text_area("Enter page content")
    if st.button("Save Page"):
        if title not in st.session_state.data["pages"]:
            page_data = {
                "title": title,
                "content": content,
                "folder": folder,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.data["pages"][title] = page_data
            if folder:
                st.session_state.data["folders"][folder].append(title)
            st.success(f"Page '{title}' created successfully!")
        else:
            st.error(f"Page '{title}' already exists!")

def view_content():
    st.subheader("View Content")
    content_type = st.radio("Select content type", ["Folders", "Pages"])
    
    if content_type == "Folders":
        folders = list(st.session_state.data["folders"].keys())
        if folders:
            selected_folder = st.selectbox("Select a folder", folders)
            st.write(f"Pages in '{selected_folder}':")
            for page in st.session_state.data["folders"][selected_folder]:
                st.write(f"- {page}")
            
            if st.button("Download Folder"):
                folder_data = {
                    "folder_name": selected_folder,
                    "pages": [st.session_state.data["pages"][page] for page in st.session_state.data["folders"][selected_folder]]
                }
                download_data = json.dumps(folder_data, indent=2)
                st.markdown(get_download_link(download_data, f"{selected_folder}.json"), unsafe_allow_html=True)
        else:
            st.write("No folders created yet.")
    
    elif content_type == "Pages":
        pages = list(st.session_state.data["pages"].keys())
        if pages:
            selected_page = st.selectbox("Select a page", pages)
            page_data = st.session_state.data["pages"][selected_page]
            st.write(f"## {page_data['title']}")
            st.write(f"Folder: {page_data['folder'] if page_data['folder'] else 'None'}")
            st.write(f"Created at: {page_data['created_at']}")
            st.write(page_data['content'])
            
            if st.button("Download Page"):
                download_data = json.dumps(page_data, indent=2)
                st.markdown(get_download_link(download_data, f"{selected_page}.json"), unsafe_allow_html=True)
        else:
            st.write("No pages created yet.")

# New function to handle download options for folders and pages
def sidebar_download_options():
    st.sidebar.subheader("Folder & Page Hierarchy")
    if st.session_state.data["folders"]:
        for folder, pages in st.session_state.data["folders"].items():
            # Folder name with a three-dot-like menu for downloading the entire folder
            with st.sidebar.expander(f"📁 {folder}"):
                if st.button(f"Download Folder '{folder}'"):
                    folder_data = {
                        "folder_name": folder,
                        "pages": [st.session_state.data["pages"][page] for page in pages]
                    }
                    download_data = json.dumps(folder_data, indent=2)
                    st.sidebar.markdown(get_download_link(download_data, f"{folder}.json"), unsafe_allow_html=True)
                for page in pages:
                    # Page name with a three-dot-like menu for downloading the page
                    st.markdown(f"   - 📄 {page}")
                    if st.button(f"Download Page '{page}'", key=f"{page}_download"):
                        page_data = st.session_state.data["pages"][page]
                        download_data = json.dumps(page_data, indent=2)
                        st.sidebar.markdown(get_download_link(download_data, f"{page}.json"), unsafe_allow_html=True)

    # Also show pages not in any folder
    standalone_pages = [page for page, data in st.session_state.data["pages"].items() if data["folder"] == ""]
    if standalone_pages:
        st.sidebar.subheader("Standalone Pages")
        for page in standalone_pages:
            st.sidebar.markdown(f"- 📄 {page}")
            if st.button(f"Download Page '{page}'", key=f"{page}_standalone_download"):
                page_data = st.session_state.data["pages"][page]
                download_data = json.dumps(page_data, indent=2)
                st.sidebar.markdown(get_download_link(download_data, f"{page}.json"), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Fénix Potion", page_icon="🐦‍🔥")
    st.title("Fénix Potion🐦‍🔥")
    
    menu = ["Create Folder", "Create Page", "View Content"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Display the folder and page hierarchy with download options in the sidebar
    sidebar_download_options()

    # Handle main menu selection
    if choice == "Create Folder":
        create_folder()
    elif choice == "Create Page":
        create_page()
    elif choice == "View Content":
        view_content()

if __name__ == "__main__":
    main()
