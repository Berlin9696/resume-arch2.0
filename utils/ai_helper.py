import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, job_description):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Analyze this resume against the job description. Provide:
                    1. Match percentage (0-100%)
                    2. 3 Key strengths
                    3. 3 Improvement suggestions
                    4. Missing keywords
                    Format using clear headings"""
                },
                {
                    "role": "user",
                    "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_description}"
                }
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing resume: {str(e)}"

def generate_interview_question(industry="Technology", experience_level="Mid-Level"):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Generate a behavioral interview question for {industry} industry targeting {experience_level} candidates using STAR method."
                }
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating question: {str(e)}"

def evaluate_star_response(answer):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Evaluate this STAR method interview answer. Provide:
                    1. Score (1-5 stars)
                    2. 3 Strengths
                    3. 3 Areas for improvement
                    4. Sample improved answer
                    Format using clear headings"""
                },
                {
                    "role": "user",
                    "content": answer
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error evaluating answer: {str(e)}"