try:
    from base_model import Model
except:
    from models.base_model import Model
import openai
import tiktoken


class OpenAI(Model):
    def __init__(self,
                 api_key: str,
                 model: str,
                 api_wait: int = 60,
                 api_retry: int = 6,
                 temperature: float = .7):
        super().__init__(api_key, model, api_wait, api_retry)

        self.temperature = temperature
        self._verify_model()
        self.set_key(api_key)
        self.encoder = tiktoken.encoding_for_model(self.model)
        self.max_tokens = self.default_max_tokens(self.model)

    def __bool__(self):
        return bool(self.api_key)

    def supported_models(self):
        return {
            "text-davinci-003": "text-davinci-003 can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports inserting completions within text.",
            "text-curie-001": "text-curie-001 is very capable, faster and lower cost than Davinci.",
            "text-babbage-001": "text-babbage-001 is capable of straightforward tasks, very fast, and lower cost.",
            "text-ada-001": "text-ada-001 is capable of very simple tasks, usually the fastest model in the GPT-3 series, and lowest cost.",
            "gpt-4": "More capable than any GPT-3.5 model, able to do more complex tasks, and optimized for chat. Will be updated with our latest model iteration.",
            "gpt-3.5-turbo": "	Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration",
        }

    def _verify_model(self):
        """
        Raises a ValueError if the current OpenAI model is not supported.
        """
        if self.model not in self.supported_models():
            raise ValueError(f"Unsupported model: {self.model}")

    def set_key(self, api_key: str):
        self._openai = openai
        self._openai.api_key = api_key

    def get_description(self):
        return self.supported_models()[self.model]

    def get_endpoint(self):
        model = openai.Model.retrieve(self.model)
        return model["id"]

    def default_max_tokens(self, model_name: str):
        token_dict = {
            "text-davinci-003": 4000,
            "text-curie-001": 2048,
            "text-babbage-001": 2048,
            "text-ada-001": 2048,
            "gpt-4": 8192,
            "gpt-3.5-turbo": 4096,
        }
        return token_dict[model_name]

    def calculate_max_tokens(self, prompt: str) -> int:

        prompt = str(prompt)
        prompt_tokens = len(self.encoder.encode(prompt))
        max_tokens = self.default_max_tokens(self.model) - prompt_tokens

        print(prompt_tokens, max_tokens)
        return max_tokens

    def run(self, prompt:str):

        if self.model in ["gpt-3.5-turbo"]:
            prompt_template = [
                {"role": "system", "content": "you are a helpful assistant."}
            ]
            prompt_template.append({"role": "user", "content": prompt})
            max_tokens = self.calculate_max_tokens(prompt_template)
            response = self._openai.ChatCompletion.create(
                model=self.model,
                messages=prompt_template,
                max_tokens=max_tokens,
                temperature=self.temperature,
            )
            return response["choices"][0]["message"]["content"].strip(" \n")

        else:
            max_tokens = self.calculate_max_tokens(prompt)
            response = self._openai.Completion.create(
                model=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=self.temperature,
            )
            return response["choices"][0]["text"].strip("\n")