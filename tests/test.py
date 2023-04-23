from llama_index import LLMPredictor, ServiceContext, GPTSimpleVectorIndex, SimpleDirectoryReader, PromptHelper
from models.openai_complete import OpenAI
from langchain.llms.base import LLM
from pathlib import Path


OPENAI_API_KEY = '<API_KEY>'
yo = OpenAI(api_key=OPENAI_API_KEY, model='gpt-3.5-turbo')


class CustomLLM(LLM):
    model_name = 'OpenAI GPT-3'

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: str = None):
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        print(prompt)
        res = yo.run(prompt)
        return res

    @property
    def _identifying_params(self):
        return {"name_of_model": self.model_name}


yo2 = CustomLLM()

def chatbot(directory_path, input_text):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=CustomLLM())

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, prompt_helper=prompt_helper)  # , embed_model=embed_model

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex.from_documents(
        documents, service_context=service_context)

    index.save_to_disk('index.json')

    index = GPTSimpleVectorIndex.load_from_disk(
        'index.json', service_context=service_context)
    response = index.query(
        input_text, response_mode="compact", service_context=service_context) #,
    return response.response


print(chatbot(Path(), 'Hi, what does the openAIComplete.py file do?'))
