import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can safely get the API key
open_api_key = os.getenv('OPENAI_API_KEY')

if not open_api_key:
    raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=open_api_key
)

def generate_daily_summary(titles):
    title_text = "\n".join(titles)
    
    prompt = f"""You are receiving a bunch of headlines of articles from an RSS feed.
    Summarize the headlines into a paragraph summary of what has been happening in the AI news you are reading.
    Do not say things like: "Here are the headlines" or "The headlines are as follows" or "Recently in AI News".
    Just start with the summary itself, and be very specific with what actuallyb happened.

    Headlines:
    {title_text}

    CONCISE SUMMARY:"""
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes news headlines."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
        max_tokens=500,
        temperature=0.2
    )


    summary = response.choices[0].message.content.strip()
    return summary