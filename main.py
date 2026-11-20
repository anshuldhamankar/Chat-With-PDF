from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
from dotenv import load_dotenv
import rag

load_dotenv()
import db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
client = genai.GenerativeModel("gemini-2.5-flash-lite")

db.init_db()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    rag.load_pdf(contents)
    return {"message": f"'{file.filename}' uploaded and indexed."}


@app.post("/chat")
async def chat(question: str = Form(...)):
    if rag.index is None:
        return {"answer": "Please upload a PDF first."}

    context_chunks = rag.retrieve(question)
    context = "\n\n".join(context_chunks)

    response = client.generate_content(f"Answer using only the provided context.\n\nContext:\n{context}\n\nQuestion: {question}")
    answer = response.text
    db.save_query(question, answer)
    return {"answer": answer}


@app.get("/history")
async def history():
    return db.get_history()
