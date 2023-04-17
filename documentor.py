import json
from pathlib import Path
import yaml
from gpt_index import (GPTSimpleVectorIndex, GPTTreeIndex, JSONReader,
                       LLMPredictor, PromptHelper, SimpleDirectoryReader)
from langchain.chat_models import ChatOpenAI
import os

class Docify:

    def __init__(self):
        os.environ["OPENAI_API_KEY"] = API_KEY
        self.cur_path = Path()

        with open('config.yaml', 'r') as f:
            conf = yaml.safe_load(f)

        self.prompt = conf['PROMPT'].format([self.cur_path.cwd().name.title()])
        self.model = conf['MODEL']

    def build_prompt_helper(self, max_input_size=4096, num_outputs=512, max_chunk_overlap=20, chunk_size_limit=600):
        prompt_helper = PromptHelper(
            max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        return prompt_helper

    def build_llm_predictor(self, llm):
        llm_predictor = LLMPredictor(llm=llm)
        return llm_predictor

    def load_data_from_path(self, directory_path):
        documents = SimpleDirectoryReader(
            directory_path, recursive=True).load_data()
        return documents

    def construct_vector_index(self, documents, llm_predictor, prompt_helper):
        index = GPTSimpleVectorIndex(
            documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        return index

    def construct_tree_index(self, documents, llm_predictor, prompt_helper):
        index = GPTTreeIndex(
            documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        return index

    def chatbot(self, index, input_text):
        response = index.query(input_text)  # response_mode='tree_summarize'
        return response.response

    def get_file_list(self, path, return_only_files: bool = False) -> list:
        files = list(filter(
            lambda path: not any(
                (part for part in path.parts if part.startswith("."))),
            path.rglob("*")
        ))
        if return_only_files:
            files = [file for file in files if file.is_file()]
        return files

    def get_tree(self) -> str:

        def build_tree(dir_path, prefix: str = ''):
            """A recursive generator, given a directory Path object
            will yield a visual tree structure line by line
            with each line prefixed by the same characters
            """
            space = '    '
            branch = '│   '
            tee = '├── '
            last = '└── '
            contents = self.get_file_list(dir_path)
            # contents each get pointers that are ├── with a final └── :
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                yield prefix + pointer + path.name
                if path.is_dir():  # extend the prefix and recurse:
                    extension = branch if pointer == tee else space
                    # i.e. space because last, └── , above so no more |
                    yield from build_tree(path, prefix=prefix+extension)

        tree_str = "\n".join(build_tree(self.cur_path))
        return tree_str

    def directory_to_dict(self, path):
        """
        Converts the contents of a directory into a dictionary using pathlib.
        """
        result = {}
        files = self.get_file_list(path)
        for entry in files:
            if entry.is_dir():
                # Recursively convert subdirectories to dictionaries
                result[entry.name] = self.directory_to_dict(entry)
            elif entry.is_file():
                # Read the contents of the file and store as value
                try:
                    with entry.open('r') as f:
                        result[entry.name] = f.read()
                except:
                    result[entry.name] = ''
        return result

    def create_index_json(self):
        tree = self.get_tree()
        dir_dict = self.directory_to_dict(self.cur_path)
        repo_dict = dict()
        repo_dict['folder structure of the repository'] = tree
        repo_dict['content of the the repository'] = dir_dict
        repo_json = json.dumps(repo_dict)
        with open('docify_index.json', 'w') as f:
            f.write(repo_json)

    def load_data_from_json(self):
        self.create_index_json()
        documents = JSONReader().load_data('docify_index.json')
        Path('docify_index.json').unlink()
        return documents

    def build_index(self):
        prompt_helper = self.build_prompt_helper()

        llm_predictor = self.build_llm_predictor(ChatOpenAI(
            temperature=0.7, model_name=self.model, max_tokens=512))
        documents = self.load_data_from_json()
        index = self.construct_vector_index(
            documents=documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        # index = self.construct_tree_index(documents=documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        return index

    def document(self):
        index = self.build_index()
        response = self.chatbot(index=index, input_text=self.prompt)
        response+="\n\n:wink: _This **README.md** was created with [Docify](https://github.com/iamadhee/docify)_"

        with open('docify_readme.md', 'w') as f:
            f.write(response)

    def debug(self):
        index = self.build_index()
        while True:
            pt = input('ask: ')
            print(self.chatbot(index=index, input_text=pt))


if __name__=='__main__':
    import sys
    API_KEY = sys.argv[1]
    docuter = Docify()
    docuter.document()
