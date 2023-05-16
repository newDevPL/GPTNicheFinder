@echo off

REM Create and activate a temporary virtual environment
python -m venv env
call env\Scripts\activate.bat

REM Upgrade pip and install required packages
python -m pip install --upgrade pip
python -m pip install pandas pytrends matplotlib pillow openai Flask scikit-learn

REM Run the Python script
python app.py

REM Deactivate and delete the temporary virtual environment
deactivate
rmdir /s /q env
