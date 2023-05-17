import openai
import os
import re
from utils import get_regions

def read_api_key(file_path="OpenAI.API"):
    print(f"Reading API key from file: {file_path}")  # DEBUG
    try:
        with open(file_path, "r") as f:
            api_key = f.readline().strip()
            print("API key read successfully")  # DEBUG
            return api_key
    except FileNotFoundError as e:
        print(f"Error reading API key: {e}")
        return None

# Set up the OpenAI API key
api_key = read_api_key()
if api_key:
    print("Setting OpenAI API key...")  # DEBUG
    openai.api_key = api_key
else:
    print("No API key found")  # DEBUG


def generate_prompt(niche, category, trends_data):
    print(f"Generating prompt for niche: {niche}, category: {category}")  # DEBUG

    # Get the relevant data from the trends_data
    max_interest = trends_data.max()[0]
    min_interest = trends_data.min()[0]
    mean_interest = trends_data.mean()[0]
    recent_interest = trends_data.iloc[-1][0]
    
    print(f"Max interest: {max_interest}, Min interest: {min_interest}, Mean interest: {mean_interest}, Recent interest: {recent_interest}")  # DEBUG

    # Read the prompt from a file
    with open('prompt.txt', 'r') as file:
        prompt = file.read()
    
    print(f"Initial prompt: {prompt}")  # DEBUG

    # Replace the placeholder variables with the actual data
    prompt = prompt.format(niche=niche,
                           recent_interest=recent_interest,
                           max_interest=max_interest,
                           min_interest=min_interest,
                           mean_interest=mean_interest,
                           category=category)
    
    print(f"Final prompt: {prompt}")  # DEBUG

    return prompt




def generate_ideas(prompt, niche, model="gpt-4", n=10):
    print(f"Generating ideas for niche: {niche}, using model: {model}")  # DEBUG
    chat_prompt = (
        f"User: {prompt}\n"
        "AI:"
    )

    print(f"Chat prompt: {chat_prompt}")  # DEBUG

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            n=n,
            stop=None,
            temperature=0.5,
        )

        print(f"Response from OpenAI API: {response}")  # DEBUG

        ideas = []
        for choice in response['choices']:
            content = choice.message.content.strip()
            matches = re.findall(r"SLOGAN: (.*?)\nSDPROMPT: (.*?)\nSCORE: (\d+)", content, re.DOTALL)
            for match in matches:
                slogan, sdprompt, score = match
                ideas.append({
                    "slogan": slogan.strip(),
                    "sdprompt": sdprompt.strip(),
                    "score": score.strip()
                })

        return ideas

    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        print("This might be due to the server being overloaded with other requests. You can retry your request, or contact OpenAI through their help center at help.openai.com if the error persists.")
        print(f"niche: {niche}")
        return []  # return an empty list instead of None
    except Exception as e:
        print(f"Error generating ideas: {e}")
        print(f"niche: {niche}")
        return []  # return an empty list instead of None
