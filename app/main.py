from fastapi import FastAPI, UploadFile, File
from .allure_parser import parse_allure_results
from .gpt_analyzer import analyze_failures
from .database import save_failure
import traceback

import zipfile, os, shutil

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        os.makedirs("uploads", exist_ok=True)  # ✅ ensure the folder exists

        zip_path = f"uploads/{file.filename}"
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

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


@app.get("/")
def read_root():
    return {"message": "MCP Server is running. Use /upload to POST Allure results."}

