@echo off
setlocal

:: Step 1: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.x.
    exit /b 1
)

:: Step 2: Install or update dependencies from requirements.txt
pip install -r requirements.txt -U
:: If a requirements.txt doesn't exist, provide an error message
if errorlevel 1 (
    echo Error installing or updating dependencies. Check requirements.txt for errors.
)

:: Step 3: Check for the existence of .env file and set environment variables
if not exist ".env" (
    echo .env file not found. Creating a sample .env file.
    (
        echo # OpenAI API Key
        echo OPENAI_API_KEY = "your-openai-api-key"
        echo.
        echo # Serper.dev API Key
        echo SERPER_API_KEY = "your-serper-api-key"
    ) > .env
    echo Please edit the .env file and add your API keys.
) else (
    :: Loop through each line in the .env file
    for /f "tokens=1,* delims==" %%x in (.env) do (
        :: Skip comments and blank lines
        if not "%%x"=="" if not "%%x"=="#" (
            :: Set environment variable using the key-value pair
            set %%x=%%y
        )
    )
)
