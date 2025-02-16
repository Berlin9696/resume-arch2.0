import os
from openai import OpenAI
from dotenv import load_dotenv
from langdetect import detect  # New import for language detection
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    """
    Generate OpenAI embeddings for given text.
    This allows semantic similarity comparison instead of relying on exact word matches.
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        return f"Error generating embedding: {str(e)}"

def calculate_match_percentage(resume_text, job_description):
    """
    Calculate similarity between resume and job description using OpenAI embeddings.
    """
    try:
        resume_embedding = get_embedding(resume_text)
        job_desc_embedding = get_embedding(job_description)

        # Ensure embeddings are valid
        if isinstance(resume_embedding, str) or isinstance(job_desc_embedding, str):
            return "Error in generating embeddings"

        # Compute cosine similarity
        similarity = np.dot(resume_embedding, job_desc_embedding) / (np.linalg.norm(resume_embedding) * np.linalg.norm(job_desc_embedding))
        return round(similarity * 100)  # Convert to percentage & remove decimals
    except Exception as e:
        return f"Error calculating match percentage: {str(e)}"

def analyze_resume(resume_text, job_description):
    """
    Analyze a resume against a job description and provide:
    1. Match percentage (0-100%)
    2. 3 Key strengths
    3. 3 Improvement suggestions
    4. Missing keywords
    The response should be in the same language as the input.
    """
    try:
        # Detect language
        resume_lang = detect(resume_text)
        job_desc_lang = detect(job_description)
        target_language = resume_lang if resume_lang == job_desc_lang else "en"

        # Compute match percentage using embeddings
        match_percentage = calculate_match_percentage(resume_text, job_description)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an expert resume analyzer. Analyze the given resume and job description. "
                        f"Ensure your response is written in {target_language}. "
                        f"Provide the following details:\n"
                        f"1. Match percentage: {match_percentage}%\n"
                        f"2. 3 Key strengths\n"
                        f"3. 3 Improvement suggestions\n"
                        f"4. Missing keywords"
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


def generate_interview_question(industry="Technology", experience_level="Mid-Level"):
    """
    Generate a behavioral interview question based on the STAR method
    specific to the given industry and experience level.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Generate a behavioral interview question for {industry} industry targeting {experience_level} candidates using the STAR method."
                }
            ],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating question: {str(e)}"

def evaluate_star_response(answer):
    """
    Evaluate a STAR method interview answer and provide:
    1. Score (1-5 stars)
    2. 3 Strengths
    3. 3 Areas for improvement
    4. A sample improved answer.
    """
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
                    Format using clear headings."""
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
