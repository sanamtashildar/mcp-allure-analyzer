
import os
import shutil
import zipfile
import traceback
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from .parser import parse_allure_results
from .gpt import analyze_failures
from .database import save_failure, fetch_failures

app = FastAPI()

@app.get("/")
def root():
    return {"message": "MCP Server is running. Use /upload to POST Allure results."}

@app.get("/favicon.ico")
def favicon():
    return JSONResponse(status_code=204, content={})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)
        zip_path = f"uploads/{file.filename}"
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if not zipfile.is_zipfile(zip_path):
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip archive")

        extract_path = zip_path.replace(".zip", "")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        failures = parse_allure_results(extract_path)
        results = []
        for failure in failures:
            reason = analyze_failures(failure)
            save_failure(failure["name"], failure["message"], reason["reason"])
            results.append(reason)
        return {"results": results}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/reports")
def get_reports():
    return fetch_failures()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("app/templates/dashboard.html") as f:
        return f.read()
    
@app.get("/")
def read_root():
    return {"message": "MCP Server is running. Use /upload to POST Allure results."}    
