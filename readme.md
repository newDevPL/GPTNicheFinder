# GPTNicheFinder - GitHub README

## Installation

1. First, clone the repository by creating a new folder on your local machine. Open your preferred command-line interface (e.g., terminal, PowerShell) or file explorer (e.g., Windows Explorer), and navigate to the newly created folder.
2. Click on `Code` at the top of the page, then click on `Download ZIP` and extract it to your desired location; or type in the following command:

```
git clone https://github.com/newDevPL/GPTNicheFinder.git
```

## Configuration

1. Navigate to the `GPTNicheFinder` folder and follow the steps below:

2. Rename the file `rename_this_to_OpenAI.API` to `OpenAI.API` and replace its content with your OpenAI API key.

3. In the `app.py` file, replace the IP in line 19 with the IP address of your computer and choose your preferred port (e.g., `app.run(host='192.168.0.10', debug=True, port=8081)`).

## Running the Application

1. Run the `start.bat` file.
2. Open your browser using the link provided in the command prompt.

## Usage

1. Choose your GPT model. GPT-4 provides slightly better and more consistent results, while GPT-3.5 Turbo is cheaper to use and not everyone can access GPT-4 yet.
2. Enter up to 5 keywords or phrases, separated by commas. Keywords will yield broader results.
3. Wait for the results, which might take up to a few minutes.

## Known Issues

- Entering more than 5 keywords or phrases will crash the application.
