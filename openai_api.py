import openai
import os

# Function to read API key from file
def read_api_key(file_path="OpenAI.API"):
    try:
        with open(file_path, "r") as f:
            return f.readline().strip()
    except FileNotFoundError as e:
        print(f"Error reading API key: {e}")
        return None

# Set up the OpenAI API key
openai.api_key = read_api_key()

def generate_prompt(niche, category, trends_data):
    # Get the relevant data from the trends_data
    max_interest = trends_data.max()[0]
    min_interest = trends_data.min()[0]
    mean_interest = trends_data.mean()[0]
    recent_interest = trends_data.iloc[-1][0]
    print(f"niche: {niche}")

    prompt = f"Generate creative t-shirt design ideas for the {niche} niche within the T-Shirt category. The niche has shown a recent increase in interest with a score of {recent_interest}. Take into account the niche's maximum interest score of {max_interest}, minimum interest score of {min_interest}, and average interest score of {mean_interest}. Consider recent trends and popular themes in this niche to create unique and catchy slogans for t-shirt designs. Based on your suggestion, also provide a prompt for Stable Diffusion meaning to generate the accompanying graphic design that would complement the slogan. Format your answer clearly."
    return prompt



def generate_ideas(prompt, niche, model="gpt-4", n=5):
    chat_prompt = (
        f"User: {prompt}\n"
        "AI:"
    )

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=n,
            stop=None,
            temperature=0.5,
        )

        return [choice.message.content.strip() for choice in response['choices']]
    except Exception as e:
        print(f"Error generating ideas: {e}")
        print(f"niche: {niche}")
        return None


