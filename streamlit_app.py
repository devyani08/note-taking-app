import streamlit as st
import base64
from datetime import datetime
import zipfile
import io
import pdfkit

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = {"folders": {}, "pages": {}}

def get_download_link(content, filename, file_type="octet-stream"):
    b64 = base64.b64encode(content).decode()
    return f'<a href="data:application/{file_type};base64,{b64}" download="{filename}">Download {filename}</a>'

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
            
            if st.button("Download Folder as ZIP"):
                download_folder_as_zip(selected_folder)
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
            
            if st.button("Download Page as PDF"):
                download_page_as_pdf(selected_page)
        else:
            st.write("No pages created yet.")

# Function to download folder as a ZIP file containing PDFs of pages
def download_folder_as_zip(folder_name):
    folder_pages = st.session_state.data["folders"].get(folder_name, [])
    
    # Create an in-memory ZIP file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for page_title in folder_pages:
            pdf_content = generate_pdf_content(page_title)
            pdf_filename = f"{page_title}.pdf"
            zip_file.writestr(pdf_filename, pdf_content)
    
    # Create download link for ZIP file
    zip_buffer.seek(0)
    b64_zip = base64.b64encode(zip_buffer.read()).decode()
    href = f'<a href="data:application/zip;base64,{b64_zip}" download="{folder_name}.zip">Download {folder_name}.zip</a>'
    st.markdown(href, unsafe_allow_html=True)

# Function to generate PDF content
def generate_pdf_content(page_title):
    page_data = st.session_state.data["pages"][page_title]
    html_content = f"""
    <html>
    <head><title>{page_data['title']}</title></head>
    <body>
    <h1>{page_data['title']}</h1>
    <p><strong>Folder:</strong> {page_data['folder']}</p>
    <p><strong>Created at:</strong> {page_data['created_at']}</p>
    <p>{page_data['content'].replace('\n', '<br>')}</p>
    </body>
    </html>
    """
    # Generate PDF content using pdfkit (HTML to PDF)
    pdf_content = pdfkit.from_string(html_content, False)
    return pdf_content

# Function to download individual page as PDF
def download_page_as_pdf(page_title):
    pdf_content = generate_pdf_content(page_title)
    st.markdown(get_download_link(pdf_content, f"{page_title}.pdf", file_type="pdf"), unsafe_allow_html=True)

# Sidebar menu for downloading
def sidebar_download_options():
    st.sidebar.subheader("Folder & Page Hierarchy")
    if st.session_state.data["folders"]:
        for folder, pages in st.session_state.data["folders"].items():
            # Folder name with download button for ZIP file
            with st.sidebar.expander(f"📁 {folder}", expanded=True):
                if st.button(f"Download Folder '{folder}' as ZIP"):
                    download_folder_as_zip(folder)
                for page in pages:
                    # Page name with a download option for PDF
                    st.sidebar.markdown(f"   - 📄 {page}")
                    if st.button(f"Download Page '{page}' as PDF", key=f"{page}_download"):
                        download_page_as_pdf(page)

    # Also show pages not in any folder
    standalone_pages = [page for page, data in st.session_state.data["pages"].items() if data["folder"] == ""]
    if standalone_pages:
        st.sidebar.subheader("Standalone Pages")
        for page in standalone_pages:
            st.sidebar.markdown(f"- 📄 {page}")
            if st.button(f"Download Page '{page}' as PDF", key=f"{page}_standalone_download"):
                download_page_as_pdf(page)

def main():
    st.set_page_config(page_title="Notion Clone with Folders", page_icon="📁")
    st.title("Notion Clone with Folders")
    
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
