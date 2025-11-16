from dotenv import load_dotenv
import os

# Load backend/.env explicitly
env_path = os.path.join(os.path.dirname(__file__), "backend/.env")
load_dotenv(env_path)

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say 'API working'"}]
)

print(response.choices[0].message.content)
