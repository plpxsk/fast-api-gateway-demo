import os

from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from mangum import Mangum
from dotenv import load_dotenv


# load ./.env for OPENAI_API_KEY
load_dotenv()


# example input data validation
class Message(BaseModel):
    text: str


app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")


@app.get("/hello")
def data():
    return {"message": "Hello from the API! Brought to you by FastAPI."}


@app.post("/chat")
def chat(message: Message):
    """Runs standard chat with OpenAI GPT"""

    # load key here, so that /hello endpoint works without it
    chat_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = "You are an expert Javascript developer, with a chill and casual attitude."

    content = message.text
    response = chat_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{content}"}
        ],
        temperature=0.7,
        max_tokens=500
    )

    assistant_message = response.choices[0].message.content

    return {"response": assistant_message}


# for AWS Lambda
handler = Mangum(app)
