import openai
import re
from llama_cpp import Llama
from pandas import DataFrame
from config import OPENAI_API_KEY, MML_MODEL_FILE

class IdeaGenerator:
    def __init__(self, api_key: str, model_file: str, prompt_file: str):
        try:
            self.model_file = model_file
            self.prompt_file = prompt_file
            self.prompt_file_path = prompt_file
            self.llama_model = None
            if model_file:
                self.llama_model = Llama(model_path=model_file)
                print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to initialize IdeaGenerator. Error: {e}")
            raise
        openai.api_key = OPENAI_API_KEY
        print("API key set successfully.")
        
    def _generate_with_llama_cpp(self, prompt: str) -> dict:
        try:
            if self.llama_model is None:
                raise ValueError("Llama model is not configured.")
            return self.llama_model(prompt, max_tokens=150, stop=["User:"],
                temperature=0.8,
                top_p=0.95,
                repeat_penalty=1.2,
                top_k=50)
        except Exception as e:
            print(f"Failed to generate with Llama CPP. Error: {e}")
            raise

    def _generate_with_openai(self, prompt: str, model: str, n: int) -> dict:
        try:
            return openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                n=1,
                stop=None,
                temperature=0.5
            )
        except Exception as e:
            print(f"Failed to generate with OpenAI. Error: {e}")
            raise

    def _generate_prompt(self, niche: str, category: str, trends_data: DataFrame) -> str:
        try:
            max_interest = trends_data.max()[0]
            min_interest = trends_data.min()[0]
            mean_interest = trends_data.mean()[0]
            recent_interest = trends_data.iloc[-1][0]

            with open(self.prompt_file_path, 'r') as file:
                prompt = file.read()

            return prompt.format(
                niche=niche,
                recent_interest=recent_interest,
                max_interest=max_interest,
                min_interest=min_interest,
                mean_interest=mean_interest,
                category=category
            )
        except Exception as e:
            print(f"Failed to generate prompt. Error: {e}")
            raise

    @staticmethod
    def _process_response(choice: dict, model_type: str) -> str:
        try:
            if model_type == "GPT":
                return choice.message.content.strip()
            elif model_type == "Llama":
                content = choice['text'].strip()
                return content.split('Example Output:\n')[-1]
            else:
                raise ValueError(f"Unknown model type: {model_type}")
        except Exception as e:
            print(f"Failed to process response. Error: {e}")
            raise

    def generate_ideas(self, niche: str, category: str, trends_data: DataFrame, model="gpt-4", n=5) -> list:
        try:
            print("Starting idea generation...")
            prompt = self._generate_prompt(niche, category, trends_data)
            
            if model == "local":
                if self.llama_model is None:
                    raise ValueError("Llama model is not configured.")
                results = [self._generate_with_llama_cpp(prompt) for _ in range(n)]
                model_type = "Llama"
            else:
                if OPENAI_API_KEY == "":
                    raise ValueError("OpenAI API key is not configured.")
                results = [self._generate_with_openai(prompt, model, n=1)]
                model_type = "GPT"

            ideas = []
            for result in results:
                if result.get('choices'):
                    for choice in result['choices']:
                        content = self._process_response(choice, model_type)
                        matches = re.findall(r"SLOGAN: (.*?)\nSDPROMPT: (.*?)\nSCORE: (\d+)", content, re.DOTALL)
                        for match in matches:
                            slogan, sdprompt, score = match
                            ideas.append({
                                "slogan": slogan.strip(),
                                "sdprompt": sdprompt.strip(),
                                "score": score.strip()
                            })

            print("Idea generation completed successfully.")
            return ideas
        except Exception as e:
            print(f"Failed to generate ideas. Error: {e}")
            raise
