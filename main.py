import os
import json
import re
from datetime import datetime
from pathlib import Path
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv
import utils


# Load environment variables
load_dotenv()

# Default model, can be overridden by environment variable
MODEL = "gemini-2.0-flash"

# System prompt for resume evaluation
SYSTEM_PROMPT = f"""
You are an expert ATS (Applicant Tracking System) resume evaluator. Analyze the provided resume and extract the following information in JSON text format:
{{
  "name": "Full name of the candidate",
  "email": "Email address found in the resume",
  "score": "Score number from 0.0 to 1.0",
  "notes": "Brief evaluation notes (max 50 words)"
}}

JOB DESCRIPTION:
{utils.load_job_description()}

Return only the JSON object, no additional text.
"""


class ResumeScorer:
    def __init__(self):
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self.client = genai.Client()

    def extract_text_from_resume(self, file_path):
        """Extract text from resume file based on extension"""
        file_extension = Path(file_path).suffix.lower()

        if file_extension == ".pdf":
            return utils.extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            return utils.extract_text_from_docx(file_path)
        elif file_extension == ".doc":
            return utils.extract_text_from_doc(file_path)
        else:
            print(f"Unsupported file format: {file_extension}")
            return None

    def evaluate_resume(self, resume_text):
        """Evaluate resume using Gemini AI"""
        try:
            response = self.client.models.generate_content(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                ),
                contents=resume_text,
            )

            # Remove markdown code blocks
            response_text = re.sub(r"```(\w+)?", "", response.text).strip()

            # Parse JSON response
            result = json.loads(response_text)

            # Validate and clean the response
            return {
                "name": result.get("name", "Unknown"),
                "email": result.get("email", "Not found"),
                "score": max(0.0, min(1.0, float(result.get("score", 0.0)))),
                "notes": result.get("notes", "No notes provided"),
            }
        except json.JSONDecodeError:
            print("Error: AI response was not valid JSON")
            return {
                "name": "Unknown",
                "email": "Not found",
                "score": 0.0,
                "notes": "Error: Failed to parse AI response",
            }

    def process_resumes(self):
        """Process all resumes in the resumes folder"""
        resumes_dir = Path("./resumes")

        if not resumes_dir.exists():
            print(f"Error: Resumes directory not found: {resumes_dir}")
            return

        # Find all resume files
        resume_files = []
        for ext in ["*.pdf", "*.docx", "*.doc"]:
            resume_files.extend(resumes_dir.glob(ext))

        if not resume_files:
            print(f"No resume files found in {resumes_dir}")
            return

        print(f"Found {len(resume_files)} resume files to process")

        # Process each resume
        results = []
        for i, file_path in enumerate(resume_files, 1):
            print(f"Processing ({i}/{len(resume_files)}): {file_path.name}")

            # Extract text
            text = self.extract_text_from_resume(file_path)
            if not text:
                print(f"  ❌ Failed to extract text from {file_path.name}")
                continue

            try:
                # Evaluate with AI
                evaluation = self.evaluate_resume(text)

                # Add to results
                results.append(
                    {
                        "filename": file_path.name,
                        "name": evaluation["name"],
                        "email": evaluation["email"],
                        "score": evaluation["score"],
                        "notes": evaluation["notes"],
                    }
                )

                print(
                    f"  ✅ Score: {evaluation['score']:.2f} | Name: {evaluation['name']}"
                )
            except Exception as e:
                print(f"  ❌ Error processing {file_path.name}: {e}")
                results.append(
                    {
                        "filename": file_path.name,
                        "name": "Unknown",
                        "email": "Not found",
                        "score": 0.0,
                        "notes": f"Error: {str(e)}",
                    }
                )
                continue

        # Save results to Excel
        self.save_to_excel(results)

        return results

    def save_to_excel(self, results):
        """Save results to Excel file"""
        # Create output directory if it doesn't exist
        output_dir = Path("./output")
        output_dir.mkdir(exist_ok=True)

        # Create DataFrame
        df = pd.DataFrame(results)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scores_{timestamp}.xlsx"
        filepath = output_dir / filename

        # Save to Excel
        df.to_excel(filepath, index=False)

        print(f"\n📊 Results saved to: {filepath}")
        print(f"📈 Processed {len(results)} resumes")

        # Display summary
        if results:
            avg_score = sum(r["score"] for r in results) / len(results)

            print(f"📊 Average score: {avg_score:.2f}")
            print(f"🏆 Highest score: {max(r['score'] for r in results):.2f}")


def main():
    """Main application entry point"""
    print("🚀 Starting ATS Resume Scorer")
    print("=" * 50)

    try:
        scorer = ResumeScorer()
        results = scorer.process_resumes()

        print("\n✅ ATS Resume Scorer completed successfully!")

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
