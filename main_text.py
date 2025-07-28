from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from gliner import GLiNER
from typing import List

'''
main_text.py is for redacting of 
text given in a text box on the html page. The corresponding html 
page for this python code is index_text.html.
main.py is for the masking/ redaction of full documents (pdfs and word docs).
'''

#Load model
print("Loading model...")
model = GLiNER.from_pretrained("urchade/gliner_small-v2.1")
print("Model loaded")

app = FastAPI()
#Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

#Define labels
labels = ["email address", "person", "organization", "location", "insurance", "address", "postal code",
          "employee id", "passport number", "phone number", "credit card number", "credit card cvv",
          "credit card expiry", "bank account number", "driver's license number", "social insurance number",
          "date of birth", "password"]


#Define Pydantic model for input data
class TextInput(BaseModel):
    text: str

#Function to redact text
def redact_text(text: str, entities: List[dict]) -> str:
    #Sort entities by start position in reverse order
    sorted_entities = sorted(entities, key=lambda e: e['start'], reverse=True)

    #Redact text
    redacted_text = text

    for entity in sorted_entities:
        start = entity['start']
        end = entity['end']
        label = f"<{entity['label']}>"
        redacted_text = redacted_text[:start] + label + redacted_text[end:]
    return redacted_text

#For HTML page
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index_text.html", "r") as f:
        return HTMLResponse(content=f.read())


#Redaction
@app.post("/redact/")
async def redact_text_endpoint(input_data: TextInput):
    #Predict entities
    predicted_entities = model.predict_entities(input_data.text, labels, threshold=0.15)

    #Redact input text based on predicted entities
    redacted_text = redact_text(input_data.text, predicted_entities)

    return {"redacted_text": redacted_text}