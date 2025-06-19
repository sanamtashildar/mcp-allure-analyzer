# MCP Server - Allure Test Failure Analyzer

## Features
- Accepts Allure report uploads
- Parses failed test cases
- Uses GPT to explain failures
- Saves results in a DB

## Running Locally
```
uvicorn app.main:app --reload
```

## Deploy
```
fly launch
fly deploy
```
