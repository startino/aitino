@echo off
for /f %%i in ('python -c "import fastapi; print(OK)"') do set result=%%i

REM Compare the result
if "%result%"=="OK" (
    echo starting dev server
) else (
    echo you are not in virtual environment or have not installed modules
    exit \b 1
)

REM Set the PYTHONPATH environment variable
set PYTHONPATH=%CD%:apps/api

REM Run Docker container
docker run -d --rm -it -p 6379:6379 redis:5-alpine

REM Run uvicorn server
python apps/api/main.py

