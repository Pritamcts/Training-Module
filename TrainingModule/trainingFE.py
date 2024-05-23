
import streamlit as st
import requests
import base64
from pathlib import Path
import time
from streamlit_pdf_viewer import pdf_viewer

# Base64 encode function
def base64_encode(byte_data):
    return base64.b64encode(byte_data).decode('utf-8')

# Define API endpoints
API_BASE_URL = "http://127.0.0.1:8000/api/" 
API_UPLOAD_URL = API_BASE_URL + "upload/"
API_EMBEDDING_URL = API_BASE_URL + "start-training/"
API_QUERY_URL = API_BASE_URL + "query/"
API_POLL_URL = API_BASE_URL + "poll/"
API_SUMMARIZE_URL = API_BASE_URL + "summarize/"  
API_FEEDBACK_URL=API_BASE_URL + "feedback/"

# Initialize session state variables
if 'summarized_result' not in st.session_state:
    st.session_state.summarized_result = ''

if 'response_summarize' not in st.session_state:
    st.session_state.response_summarize = None

if 'result' not in st.session_state:
    st.session_state.result=[]

if 'prompt' not in st.session_state:
    st.session_state.prompt= ''

if 'pdf_viewer_open' not in st.session_state:
    st.session_state.pdf_viewer_open = False

# Define common headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic d2ViOnBhbm5hMTIz"
}

# Function to check if a string contains numbers
def contains_numbers(string):
    return any(char.isdigit() for char in string)

# Hide Streamlit style elements
hide_st_style = """
        <style>
        #MainMenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)

# UI Rendering Function
def render_ui():
    st.title("📚 Training Module Interface")

    st.subheader("Upload Training Material")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        author = st.text_input("Author", key="author_input")

    with col2:
        publisher = st.text_input("Publisher", key="publisher_input")

    with col3:
        url = st.text_input("URL (optional)", key="url_input")

    with col4:
        material_type = st.selectbox("Select Material Type", ["Research Paper", "Book", "Cheat Sheet", "Parental Guide"])

    uploaded_file = None
    if author and publisher and material_type and (not contains_numbers(author)) and (not contains_numbers(publisher)):
        uploaded_file = st.file_uploader("Choose File", type=['pdf', 'mp3', 'mp4', 'txt', 'html'])

    if not author or not publisher or not material_type:
        st.info("Author, Publisher, Material Type, and User Type are mandatory.")

    elif contains_numbers(author) or contains_numbers(publisher):
        st.error("Author and Publisher cannot contain numbers.")
    else:
        if uploaded_file or url.strip() != '':
            if uploaded_file:
                filename = uploaded_file.name
                filetype = uploaded_file.type
                file_path = Path(filename)
                file_stem = file_path.stem  # The file name without the extension
                file_extension = file_path.suffix  # The file extension
                filebody = base64_encode(uploaded_file.getvalue())

                # Prepare the request body
                data = {
                    "filename": file_stem,
                    "filetype": file_extension[1:],
                    "filebody": filebody,
                    "author": author,
                    "publisher": publisher,
                    "material_type": material_type,
                    "url": url.strip()
                }

                # Make the POST request
                response_upload = requests.post(API_UPLOAD_URL, json=data, headers=headers)

                # Check if request was successful
                if len(str(response_upload.status_code)) == 3 and str(response_upload.status_code)[0] == '2':
                    st.success("✅ File uploaded successfully!")
                else:
                    st.error(f"❌ Failed to upload file. Status code: {response_upload.status_code}")

    # Start Embedding Button
    if uploaded_file is not None and st.button("🚀 Start Embedding"):
        with st.spinner("Embedding in progress..."):
            # Data for the request body
            data = {
                "embed": "all"
            }

            # Make the POST request for starting embedding
            response_embedding = requests.post(API_EMBEDDING_URL, json=data, headers=headers)

            # Check if request was successful
            if len(str(response_embedding.status_code)) == 3 and str(response_embedding.status_code)[0] == '2':
                st.success("🎉 Embedding done successfully!")
            else:
                st.error(f"❌ Failed to start embedding. Status code: {response_embedding.status_code}")

    # Query Knowledge DB
    st.subheader("🔍 Query Knowledge DB")
    with st.form(key='query_form'):
        user_type = st.selectbox("Select User Type", ["BCBA", "Parent", "RBT"], key="user_type_input")

        st.session_state.prompt = st.text_input("Enter your query", key="query_input")
        submit_button = st.form_submit_button(label='Search')
        if submit_button:
            query_knowledge_db(user_type)

    if st.session_state.response_summarize is not None and st.session_state.response_summarize.status_code == 200:
        st.session_state.summarized_result = st.session_state.response_summarize.json()['summary']
        st.subheader("Summarized Result:")
        st.write(st.session_state.summarized_result)
        # Display source file details
        if (len(st.session_state.result[0]["source"])) > 0:
            st.markdown("**More detail about this can be found in the following Documents:**")
            for i, item in enumerate (st.session_state.result[0]["source"]):
                # Display source information
                filename = item.get("file-name", "None")
                author = item.get("creator", "None")
                publisher = item.get("owner", "None")
                url = item.get("url", "None")
                material_type = item.get("material-type", "None")
                
                button_key = f"view_pdf_{i}_{filename}"
                if st.button(f"View PDF: {filename}", key=button_key):
                    # Fetch the PDF file from the server
                    pdf_data = fetch_pdf(filename)
                    if pdf_data is not None:
                        # Store the PDF data in session state
                        st.session_state.pdf_data = pdf_data
                        st.session_state.pdf_viewer_open = True
                    else:
                        st.error("Failed to fetch PDF file.")
   
                st.write(f"**Author:** {author}")
                st.write(f"**Publisher:** {publisher}")
                st.write(f"**URL:** {url}")
                st.write(f"**Material Type:** {material_type}")
                st.write("-" * 50)

        if "pdf_data" in st.session_state:
            st.subheader("PDF Viewer: ")
            close_button = st.button("Close PDF")
            if close_button:
                st.session_state.pdf_viewer_open = False
                del st.session_state["pdf_data"]
            if st.session_state.pdf_viewer_open:
                pdf_viewer(st.session_state.pdf_data, width=700)
            else:
                st.write("PDF viewer is closed.")

        feedback()

def feedback():
    st.title("Rate and Give Feedback")

    # Rating
    feedback = ''
    if 'rating' not in st.session_state:
        st.session_state.rating = None
    columns = st.columns(5)

    with columns[0]:
        if st.button("😞"):
            st.success("Very Sad")
            st.session_state.rating = 1

    with columns[1]:
        if st.button("😔"):
            st.success("Sad")
            st.session_state.rating = 2

    with columns[2]:
        if st.button("😐"):
            st.success("Neutral")
            st.session_state.rating = 3

    with columns[3]:
        if st.button("😊"):
            st.success("Happy")
            st.session_state.rating = 4
    with columns[4]:
        if st.button("😍"):
            st.success("Very Happy")
            st.session_state.rating = 5

    st.subheader("Feedback")
    feedback = st.text_area("Please leave your feedback here:")
    
    if st.button("Submit"):
        if st.session_state.rating is not None:
            # Send rating and feedback to Flask endpoint
            submit_feedback(st.session_state.rating, feedback)
            st.success("Thank you for your feedback!")
            feedback=''
        else:
            st.error("Please select a rating before submitting.")

def submit_feedback(rating, feedback):
    # Define the data to be sent to the Flask endpoint
    if feedback == '':
        feedback = 'NULL'
    data = {
        'rating': rating,
        'feedback': feedback
    }
    
    # Send POST request to the Flask endpoint
    response = requests.post(API_FEEDBACK_URL, json=data,headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        st.success("Feedback submitted successfully")
    else:
        st.error(f"Failed to submit feedback: {response.content}")

def query_knowledge_db(user_type):
    # Use a spinner while waiting for the response
    with st.spinner("Searching..."):
        # Data for the request body
        data = {
            "prompt": st.session_state.prompt,
            "user_type":user_type
        }

        # Make the POST request for querying knowledge DB
        response_query = requests.post(API_QUERY_URL, json=data, headers=headers)

        # Check if request was successful
        if len(str(response_query.status_code)) == 3 and str(response_query.status_code)[0] == '2':
            result = response_query.json()
            print(result)
            if result['uid'] !='irrelevant':
                task_id = result["uid"]
                placeholder = st.empty()
                placeholder.text('Summarizing the result ...')
                time.sleep(5)
                result_response = ''
                # Polling for results
                while True:
                    result_response = requests.post(API_POLL_URL, json={'uid': task_id}, headers=headers)
                    if result_response.status_code == 200 and result_response.json()['status'] == 'DONE':
                        break
                    else:
                        time.sleep(2)  # Wait for a second before polling again

                st.session_state.result = result_response.json()['Data']
                # Prepare data to send to the summarize API endpoint
                summarize_data = {
                    'results': st.session_state.result
                }

                # Make a POST request to the summarize API endpoint
                st.session_state.response_summarize = requests.post(API_SUMMARIZE_URL, json=summarize_data, headers=headers)
                placeholder.text('')
            else:
                st.error("Irrelevant")
        else:
            st.error(f"❌ Failed to perform query. Status code: {response_query.status_code}")

def fetch_pdf(filename):
    # Define the URL to fetch the PDF file from the server
    pdf_url = f"{API_BASE_URL}view-pdf/{filename}/"
    
    # Make a GET request to fetch the PDF file
    response = requests.get(pdf_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Store the PDF data in session state
        return response.content
    else:
        # Return None if the request failed
        st.error(f"Failed to fetch PDF file: {response.status_code}")
        return None
    
if __name__ == "__main__":
    render_ui()

