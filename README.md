# AI Based Resume Analuzer
 
# AI Resume Analyzer

## Overview
AI Resume Analyzer is a web application built using Streamlit. It allows users to upload their resumes in PDF format and receive insightful feedback, skill recommendations, and job-specific course suggestions. It also provides video tutorials on resume writing and interview preparation. The app has two main user roles: **User** and **Admin**.

## Features

### User Features:
- Upload and analyze resumes in PDF format.
- Receive a detailed resume analysis, including:
  - Resume score based on content.
  - Predicted career field.
  - Recommended skills for improvement.
  - Suggested courses to enhance job-specific skills.
- View PDF resumes within the app.
- Get tips on improving resumes and boosting job prospects.
- Watch videos on resume writing and interview preparation.

### Admin Features:
- View and manage user data stored in a MySQL database.
- Download user data as a CSV file.
- Visualize user data insights using charts.

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** MySQL
- **APIs:** YouTube Data API for fetching video titles

## Installation

### Prerequisites:
- Python 3.7 or higher
- MySQL Server

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```
2. Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Update the database credentials in the code.
   - Ensure the database `cv` and table `user_data` are created during runtime.

4. Set up YouTube Data API:
   - Generate an API key from the [Google Cloud Console](https://console.cloud.google.com/).
   - Replace `YOUTUBE_API_KEY` in the code with your API key.

5. Run the application:
   ```bash
   streamlit run app.py
   ```
6. Access the application in your browser at `http://localhost:8501`.

## Usage
1. **User Role:**
   - Upload your resume in PDF format.
   - View the analysis, recommendations, and tips.
   - Watch bonus videos for resume writing and interview preparation.

2. **Admin Role:**
   - Log in using admin credentials (default: username: `Harsh25`, password: `12345678`).
   - View user data, download reports, and generate insights.

## Folder Structure
```
.
|-- app.py                     # Main application file
|-- requirements.txt           # Required Python libraries
|-- Uploaded_Resumes/          # Directory to store uploaded resumes
|-- Logo/                      # Directory for application logos
|-- Courses.py                 # Course recommendation data
```

## Requirements File
```
streamlit
pandas
pymysql
nltk
pyresparser
pdfminer.six
streamlit-tags
Pillow
pafy
plotly
requests
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Streamlit](https://streamlit.io/)
- [Google YouTube API](https://developers.google.com/youtube/)
- [PyResParser](https://github.com/OmkarPathak/pyresparser)

---