""" Server-side application. Contains various endpoints to record and return. """
""" For a single user. """
from fastapi import FastAPI
from pydantic import BaseModel

# System
import os

# Built
from name_recognizer import NameClassifier
import gmail

# Documentation
from typing import List

app = FastAPI()
gen = gmail.getResults()
messages = []
personMessages = []

INIT_FP = os.path.join("..", "backend", "init", "paths.ini")
PICKLE = os.path.join("..", "backend", "init", "token.pickle")
CLIENT_SECRET = os.path.join("..", "backend", "init", "client_token.json")

class Sender(BaseModel):
    sender: str

@app.get("/") # Root
def root():
    return "Go to /docs for the docs"

@app.get("/fetch_emails")
async def fetch_emails_prototype():
    """ Fetch the emails, 50 at a time (Gmail application limit) """
    for messageGroup in gen:
        messages.append(messageGroup)
        for message in messageGroup:
            if NameClassifier(message["from"]).get_decision():
                personMessages.append(message)
        return messageGroup

@app.get("/person_emails")
def person_emails() -> List[dict]:
    return personMessages
