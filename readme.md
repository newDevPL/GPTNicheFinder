# GPTNicheFinder - GitHub README

Welcome to GPTNicheFinder, a robust niche research tool underpinned by Google Trends data and OpenAI's GPT model. This application presents a streamlined methodology for identifying profitable niche markets, utilizing data-driven insights, and the cutting edge of artificial intelligence. It is an ideal tool for entrepreneurs, marketers, and enthusiasts seeking undiscovered opportunities. GPTNicheFinder is designed to facilitate your search.

# Key Features:

Google Trends Integration: GPTNicheFinder leverages Google Trends data, including interest over time, related queries, and suggestions, to analyze emerging trends and pinpoint niche opportunities. This comprehensive approach guarantees you a panoramic view of the market landscape.

OpenAI's GPT Model: Utilizing the power of OpenAI's GPT model, GPTNicheFinder generates niche ideas that align seamlessly with your chosen keywords. The model generates innovative prompts and slogans, equipping you with valuable insights for your niche exploration.

Flask Web Interface: The intuitive Flask-based web interface allows you to input up to 5 keywords or phrases conveniently and receive niche suggestions in real-time. The interface is designed for effortless navigation.

Customization and Flexibility: GPTNicheFinder provides customization options, including the capacity to configure the IP address and port to accommodate your environment. This flexibility ensures seamless integration into your current workflow.

## Installation

1. Initiate the process by cloning the repository. Create a new folder on your local machine and navigate to it using your preferred command-line interface (e.g., terminal, PowerShell) or file explorer (e.g., Windows Explorer).
2. Click on Code at the top of the page, then click on Download ZIP and extract the file to your chosen location. Alternatively, input the following command:

```
git clone https://github.com/newDevPL/GPTNicheFinder.git
```
Please be aware: If you wish to utilize the local model option, you are required to procure your own Llama model. These models are readily available from numerous sources, one of the most prominent being HuggingFace. It is crucial to ensure that the model adheres to the latest Llama format. Unfortunately, models in the old format will not be compatible. While we have successfully tested the app with the `ggml-gpt4-x-vicuna-13b-q5_1.bin` model, it should be operational with other models as well.

## Configuration

1. Traverse to the GPTNicheFinder folder and implement the steps below:

2. Execute the `setup.bat` file on Windows or `setup.sh` file on Linux and Mac. Input your `Open AI API key`, `path to your local llama model`, `your local IP address` and the desired `port`. The app can be run with either the GPT or Llama model or both, thereby making the app potentially free to use.

## Running the Application

1. Run the `start.bat` file on Windows or `start.sh` file on Linux and Mac.
2. Open your browser and input the link that the command prompt provides. This link should include the IP and Port you specified when executing `setup.bat` or `setup.sh`.For example, it should look something like this: http://YourIPAddress:PortNumber.

## Usage

1. Select your GPT or Llama model. While the GPT-4 model yields slightly superior and consistent results, the GPT-3.5 Turbo model is more affordable and accessible. Llama models, though slower and less accurate, are free to use. However, the efficiency of the model largely depends on your computer's performance.
2. Input up to 5 keywords or phrases, each separated by a comma. Keywords will generate broader results.
3. Patiently wait for the results, which may take a few minutes.

## Known Issues

- None

## Contributing:

We warmly welcome contributions to GPTNicheFinder! If you have ideas for enhancements, bug fixes, or new features, please contribute by submitting a pull request. Your contributions will enrich the tool and augment its value for the community.

## License:

GPTNicheFinder is released under the Unlicense license, granting you the freedom to use, modify, and distribute the application without any restrictions. You can find the license details in the repository.


If you like this project, consider donating some ETH: 0x202580B9639D6434316DBabcbadDE5a246468125

