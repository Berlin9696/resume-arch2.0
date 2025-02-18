import os
import logging
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from langdetect import detect  # Language detection for better response formatting

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_embedding(text):
    """
    Generate OpenAI embeddings for given text to allow semantic similarity comparison.
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",  # Updated model for better embeddings
            input=text
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        return None

def calculate_match_percentage(resume_text, job_description):
    """
    Calculate similarity between resume and job description using OpenAI embeddings.
    """
    try:
        resume_embedding = get_embedding(resume_text)
        job_desc_embedding = get_embedding(job_description)

        if resume_embedding is None or job_desc_embedding is None:
            return "Error in generating embeddings"

        # Compute cosine similarity
        similarity = np.dot(resume_embedding, job_desc_embedding) / (
            np.linalg.norm(resume_embedding) * np.linalg.norm(job_desc_embedding)
        )

        return round(similarity * 100)  # Convert to percentage
    except Exception as e:
        logging.error(f"Error calculating match percentage: {e}")
        return "Error calculating match percentage"

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
        # Detect language to ensure AI response matches input language
        resume_lang = detect(resume_text)
        job_desc_lang = detect(job_description)
        target_language = resume_lang if resume_lang == job_desc_lang else "en"

        # Compute match percentage
        match_percentage = calculate_match_percentage(resume_text, job_description)

        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Optimized for better responses
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are an expert resume analyzer. Analyze the given resume and job description. "
                        f"Ensure your response is in {target_language}. Provide:\n"
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
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error analyzing resume: {e}")
        return "Error analyzing resume"

def generate_interview_question(industry="Technology", experience_level="Mid-Level"):
    """
    Generate a behavioral interview question based on the STAR method.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Generate a STAR method behavioral interview question for {industry} targeting {experience_level} candidates."
                }
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating interview question: {e}")
        return "Error generating interview question"

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
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Evaluate this STAR method interview answer. Provide:
                    1. Score (1-5 stars)
                    2. 3 Strengths
                    3. 3 Areas for improvement
                    4. Sample improved answer
                    Format the response with clear headings."""
                },
                {
                    "role": "user",
                    "content": answer
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error evaluating answer: {e}")
        return "Error evaluating answer"


def generate_resume(user_answer):
    try:
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {
                    "role": "system",
                    "content": "You are a resume generation assistant. Based on the user's answer, generate a professional resume."
                },
                {
                    "role": "user",
                    "content": f"USER'S INPUT: {user_answer}"
                }
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()  # Ensure response is clean

    except Exception as e:
        print("Error in generate_resume:", str(e))  # Debugging log
        return f"Error generating resume: {str(e)}"