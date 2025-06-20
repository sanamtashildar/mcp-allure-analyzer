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
        print("[UPLOAD] Creating uploads directory if not exists...")
        os.makedirs("uploads", exist_ok=True)
        zip_path = f"uploads/{file.filename}"
        print(f"[UPLOAD] Saving uploaded file to {zip_path}")
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"[UPLOAD] Checking if {zip_path} is a valid zip file...")
        if not zipfile.is_zipfile(zip_path):
            print("[UPLOAD] Uploaded file is not a valid zip archive!")
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip archive")

        extract_path = zip_path.replace(".zip", "")
        print(f"[UPLOAD] Extracting zip to {extract_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        print(f"[UPLOAD] Listing subdirectories in {extract_path}")
        subdirs = [d for d in os.listdir(extract_path) if os.path.isdir(os.path.join(extract_path, d))]
        print(f"[UPLOAD] Subdirectories found: {subdirs}")
        results_path = extract_path
        if len(subdirs) == 1 and subdirs[0] == "results":
            results_path = os.path.join(extract_path, "results")
            print(f"[UPLOAD] Using nested results path: {results_path}")
        else:
            print(f"[UPLOAD] Using extract path as results path: {results_path}")

        print(f"[UPLOAD] Listing files in {results_path}")
        print(os.listdir(results_path))
        failures = parse_allure_results(results_path)
        print(f"[UPLOAD] Failures found: {failures}")
        results = []
        for failure in failures:
            print(f"[UPLOAD] Analyzing failure: {failure}")
            reason = analyze_failures(failure)
            print(f"[UPLOAD] Reason from GPT: {reason}")
            save_failure(failure["name"], failure["message"], reason["reason"])
            results.append(reason)
        print(f"[UPLOAD] Returning results: {results}")
        return {"results": results}

    except Exception as e:
        print(f"[UPLOAD] Exception occurred: {e}")
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
