# ATS Resume Score Agent

A simple and fast Applicant Tracking System (ATS) resume scorer using Google Gemini AI. This tool evaluates resumes and provides structured scoring with name extraction, email detection, and some feedback.

## Features

- 📄 Supports PDF and Word document formats (.pdf, .docx, .doc)
- 🤖 AI-powered evaluation using Google Gemini
- 📊 Structured output with scoring (0-1 scale)
- 📈 Excel export with detailed results
- 🚀 Fast batch processing
- 📝 Comprehensive logging

## Project Structure

```
ats-resume-score-agent/
├── resumes/                 # Place resume files here
├── output/                  # Excel output files
├── .env                     # API keys
├── main.py                  # Main application entry point
├── job_description.txt      # Job requirements file
...
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get your Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Rename `.env.sample` to `.env` file and replace `your_google_api_key_here` with your actual API key:

### 3. Add Resume Files

Place your resume files (PDF, DOCX, DOC) in the `./resumes/` folder.

### 4. Run the Application

```bash
python main.py
```

## Output Format

The tool generates an Excel file in the `./output/` folder with the following:

- **Name**: Extracted candidate name
- **Email**: Extracted email address
- **Score**: ATS score (0.0 to 1.0)
- **Notes**: AI-generated evaluation notes
- **Processing Date**: When the resume was processed

## License

This project is licensed under the MIT License. See the [MIT License](LICENSE) file.
