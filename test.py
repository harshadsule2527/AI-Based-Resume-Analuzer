import streamlit as st
import pandas as pd
import base64
import random
import time, datetime
import requests
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
import pafy
import plotly.express as px
import nltk

nltk.download('stopwords')

YOUTUBE_API_KEY = 'AIzaSyDuZCC61oeN4LUO7NPbvj2md3vNXs4kZxU'

def fetch_yt_video(video_id):
    youtube_api_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={YOUTUBE_API_KEY}&part=snippet'
    response = requests.get(youtube_api_url)
    video_info = response.json()
    
    if video_info["items"]:
        video_title = video_info["items"][0]["snippet"]["title"]
        return video_title
    else:
        return "Title not found"

def get_table_download_link(df, filename, text):
    """Generates a download link for a DataFrame."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # encoding as base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

# Database connection
connection = pymysql.connect(host='localhost', port=3306, user='root', password='1234'.encode('utf-8'), db='cv')
cursor = connection.cursor()

def insert_data(name, email, res_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, str(res_score), timestamp, str(no_of_pages), reco_field, cand_level, skills, recommended_skills, courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

# Streamlit app
st.set_page_config(
   page_title="AI Resume Analyzer",
   page_icon='./Logo/logo2.png',
)

def run():
    st.title("AI Resume Analyzer")
    st.sidebar.title("Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities, key="user_choice")

    link = '[©Developed by Harsh](https://www.linkedin.com/in/harsh-adsule-m2527/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)

    # Create DB and table
    db_sql = """CREATE DATABASE IF NOT EXISTS CV;"""
    cursor.execute(db_sql)

    DB_table_name = 'user_data'
    table_sql = f"""
    CREATE TABLE IF NOT EXISTS {DB_table_name} (
        ID INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(500) NOT NULL,
        Email_ID VARCHAR(500) NOT NULL,
        resume_score VARCHAR(8) NOT NULL,
        Timestamp VARCHAR(50) NOT NULL,
        Page_no VARCHAR(5) NOT NULL,
        Predicted_Field BLOB NOT NULL,
        User_level BLOB NOT NULL,
        Actual_skills BLOB NOT NULL,
        Recommended_skills BLOB NOT NULL,
        Recommended_courses BLOB NOT NULL,
        PRIMARY KEY (ID)
    );
    """
    cursor.execute(table_sql)

    if choice == 'User':
        st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume and get smart recommendations</h5>''', unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"], key="resume_uploader")
        
        if pdf_file is not None:
            with st.spinner('Uploading your Resume...'):
                time.sleep(4)
            save_image_path = './Uploaded_Resumes/' + pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            
            if resume_data:
                resume_text = pdf_reader(save_image_path)
                st.header("**Resume Analysis**")
                st.success(f"Hello {resume_data['name']}")
                st.subheader("**Your Basic Info**")
                
                try:
                    st.text(f"Name: {resume_data['name']}")
                    st.text(f"Email: {resume_data['email']}")
                    st.text(f"Contact: {resume_data['mobile_number']}")
                    st.text(f"Resume pages: {str(resume_data['no_of_pages'])}")
                except:
                    pass

                # Determine candidate level based on number of pages
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at Intermediate level!</h4>''', unsafe_allow_html=True)
                else:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Experience level!</h4>''', unsafe_allow_html=True)

                # Skills recommendation
                st_tags(label='### Your Current Skills', text='See our skills recommendation below', value=resume_data['skills'], key='current_skills')

                # Skill recommendations and field determination logic
                recommended_skills = []
                reco_field = ''
                rec_course = ''

                if any(skill.lower() in ['tensorflow', 'keras', 'pytorch'] for skill in resume_data['skills']):
                    reco_field = 'Data Science'
                    st.success("**Our analysis says you are looking for Data Science Jobs**")
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling']
                    rec_course = course_recommender(ds_course)
                # Similar logic for other fields (Web Development, Android Development, etc.)

                # Resume Score logic
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score += 20
                # Add other conditions for 'Declaration', 'Hobbies', etc.
                
                # Final Resume Score display
                st.progress(resume_score)
                st.success(f"Your Resume Writing Score: {resume_score}")

                # Save data to the database
                ts = time.time()
                timestamp = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S'))
                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp, str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']), str(recommended_skills), str(rec_course))

                # Video recommendations
                resume_vid = random.choice(resume_videos)
                res_vid_title = fetch_yt_video(resume_vid)
                st.subheader(f"✅ {res_vid_title}")
                st.video(resume_vid)

    else:
        # Admin side
        st.success('Welcome to Admin Side')

        ad_user = st.text_input("Username", key="admin_username")
        ad_password = st.text_input("Password", type='password', key="admin_password")

        if st.button('Login'):
            if ad_user == 'admin' and ad_password == 'admin':
                st.success("Welcome Harsh")
                # Add admin functionalities here

if __name__ == '__main__':
    run()
