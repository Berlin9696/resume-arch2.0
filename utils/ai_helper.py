import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, job_description):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert resume analyzer. Analyze the given resume and job description, "
                        "which may be written in different languages, and output your analysis in the language "
                        "that the user provided. Translate to English only if needed, but do not include any markdown "
                        "or extra formatting characters this is crucial to remove them (such as '#' or '*') in your output. "
                        "Please provide the following in plain text with clear headings:\n"
                        "1. Match percentage (0-100%)\n"
                        "2. 3 Key strengths\n"
                        "3. 3 Improvement suggestions\n"
                        "4. Missing keywords"
                    )
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