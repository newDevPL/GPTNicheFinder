@echo off

REM Check if config.py exists
IF NOT EXIST config.py (
    REM config.py doesn't exist, create a new one with default values
    (
        echo # Configuration file
        echo.
        echo # OpenAI API key
        echo OPENAI_API_KEY = ""
        echo.
        echo # MML model file path
        echo MML_MODEL_FILE = ""
        echo.
        echo # Prompt file path
        echo PROMPT_FILE = "prompt.txt"
        echo.
        echo # IP address and port
        echo IP_ADDRESS = ""
        echo PORT = 8081
    ) > config.py
)

REM Read the existing values from config.py
FOR /F "tokens=1,* delims==" %%G IN (config.py) DO (
    IF "%%G"=="OPENAI_API_KEY" SET EXISTING_OPENAI_API_KEY=%%H
    IF "%%G"=="MML_MODEL_FILE" SET EXISTING_MML_MODEL_FILE=%%H
    IF "%%G"=="IP_ADDRESS" SET EXISTING_IP_ADDRESS=%%H
    IF "%%G"=="PORT" SET EXISTING_PORT=%%H
)

REM Prompt the user for new values if they don't exist or ask to use existing values
SET "OPENAI_API_KEY=%EXISTING_OPENAI_API_KEY%"
IF "%OPENAI_API_KEY%"=="" (
    SET /P "OPENAI_API_KEY=Enter the OpenAI API key: "
)

SET "MML_MODEL_FILE=%EXISTING_MML_MODEL_FILE%"
IF "%MML_MODEL_FILE%"=="" (
    SET /P "MML_MODEL_FILE=Enter the MML model file path: "
)

SET "PROMPT_FILE=prompt.txt"

SET "IP_ADDRESS=%EXISTING_IP_ADDRESS%"
IF "%IP_ADDRESS%"=="" (
    SET /P "IP_ADDRESS=Enter the IP address: "
)

SET "PORT=%EXISTING_PORT%"
IF "%PORT%"=="" (
    SET /P "PORT=Enter the port: "
)

REM Write the updated values to config.py
(
    echo # Configuration file
    echo.
    echo # OpenAI API key
    echo OPENAI_API_KEY = "%OPENAI_API_KEY%"
    echo.
    echo # MML model file path
    echo MML_MODEL_FILE = "%MML_MODEL_FILE%"
    echo.
    echo # Prompt file path
    echo PROMPT_FILE = "%PROMPT_FILE%"
    echo.
    echo # IP address and port
    echo IP_ADDRESS = "%IP_ADDRESS%"
    echo PORT = %PORT%
) > config.py
