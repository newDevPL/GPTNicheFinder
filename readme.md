# GPTNicheFinder - GitHub README

Welcome to GPTNicheFinder, a powerful niche research tool powered by Google Trends data and OpenAI's GPT model. This application provides a streamlined approach to identify profitable niche markets by leveraging data-driven insights and cutting-edge artificial intelligence. Whether you're an entrepreneur, marketer, or enthusiast looking for untapped opportunities, GPTNicheFinder is here to assist you.

# Key Features:

Google Trends Integration: GPTNicheFinder fetches Google Trends data, including interest over time, related queries, and suggestions, to analyze emerging trends and identify niche opportunities. This comprehensive approach ensures that you have a holistic view of the market landscape.

OpenAI's GPT Model: By harnessing the power of OpenAI's GPT model, GPTNicheFinder generates niche ideas that are highly relevant and aligned with your chosen keywords. The model generates creative prompts and slogans, providing you with valuable insights to kickstart your niche exploration.

Flask Web Interface: The user-friendly Flask-based web interface enables you to easily input up to 5 keywords or phrases and receive niche suggestions in real-time. The interface is intuitive, allowing you to navigate through the app effortlessly.

Customization and Flexibility: GPTNicheFinder offers customization options, including the ability to configure the IP address and port to match your environment. This flexibility ensures seamless integration into your existing workflow.

## Installation

1. First, clone the repository by creating a new folder on your local machine. Open your preferred command-line interface (e.g., terminal, PowerShell) or file explorer (e.g., Windows Explorer), and navigate to the newly created folder.
2. Click on `Code` at the top of the page, then click on `Download ZIP` and extract it to your desired location; or type in the following command:

```
git clone https://github.com/newDevPL/GPTNicheFinder.git
```

## Configuration

1. Navigate to the `GPTNicheFinder` folder and follow the steps below:

2. Rename the file `rename_this_to_OpenAI.API` to `OpenAI.API` and replace its content with your OpenAI API key.

3. In the `app.py` file, replace the IP in line 48 with the IP address of your computer and choose your preferred port (e.g., `app.run(host='192.168.0.10', debug=True, port=8081)`).

## Running the Application

1. Run the `start.bat` file.
2. Open your browser using the link provided in the command prompt.

## Usage

1. Choose your GPT model. GPT-4 provides slightly better and more consistent results, while GPT-3.5 Turbo is cheaper to use and not everyone can access GPT-4 yet.
2. Enter up to 5 keywords or phrases, separated by commas. Keywords will yield broader results.
3. Wait for the results, which might take up to a few minutes.

## Known Issues

- None

## Contributing:

Contributions to GPTNicheFinder are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to contribute by submitting a pull request. Your contributions will help enhance the tool and make it even more valuable for the community.

## License:

GPTNicheFinder is released under the Unlicense license, which allows you to use, modify, and distribute the application without any restrictions. You can find the license details in the repository.
