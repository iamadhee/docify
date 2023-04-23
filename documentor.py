import json
from pathlib import Path
import yaml
from llama_index import LLMPredictor, ServiceContext, GPTSimpleVectorIndex, SimpleDirectoryReader, PromptHelper, JSONReader, GPTTreeIndex, LangchainEmbedding
from langchain.llms.base import LLM
from models.openai_complete import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from tqdm import tqdm


with open('config.yaml','r') as f:
    config = yaml.safe_load(f)

class DocLLM(LLM):
    model_name = config['MODEL']

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: str = None):
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        chatbot = model_llm
        res = chatbot.run(prompt)
        return res

    @property
    def _identifying_params(self):
        return {"name_of_model": self.model_name}


class ReadmeGen:

    def __init__(self):

        self.cur_path = Path()
        self.prompt = config['PROMPT'].format([self.cur_path.cwd().name.title()])
        self.model = DocLLM()

    def contextbot(self, index, input_text):
        response = index.query(
            input_text, response_mode="compact", service_context=self.build_context())
        return response.response

    def chatbot(self, input_text):
        response = self.model(input_text)
        return response

    def build_context(self, max_input_size = 4096, num_outputs = 512,  max_chunk_overlap = 20, chunk_size_limit = 600):
        prompt_helper = PromptHelper(
            max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

        llm_predictor = LLMPredictor(llm=self.model)

        service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor, prompt_helper=prompt_helper) 

        return service_context

    
    def build_summary_dict(self):
        files = self.get_file_list(self.cur_path,return_only_files=True)
        summary_dict = dict()

        for file in tqdm(files):
            try:
                with open(file,'r') as f:
                    contents = f.read()
            except:
                continue

            if len(contents) < 10:
                continue

            prompt = "Summarize what the below code does: \n ```"+contents+"\n```"

            response = self.chatbot(prompt)
            summary_dict[str(file)] = response

        return summary_dict

    def build_index(self, save=False):
        service_context = self.build_context()
        tree = self.get_tree()
        sum_dict = self.build_summary_dict()
        # dir_dict = self.directory_to_dict(self.cur_path)
        repo_dict = dict()
        repo_dict['folder structure'] = tree
        repo_dict['summary of files'] = sum_dict
        repo_json = json.dumps(repo_dict)
        with open('indices/readme_index.json', 'w') as f:
            f.write(repo_json)

        documents = JSONReader().load_data('indices/readme_index.json')

        index = GPTSimpleVectorIndex.from_documents(
            documents, service_context=service_context)

        if not save:
            Path('indices/readme_index.json').unlink()

        return index

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
        with open('indices/readme_index.json', 'w') as f:
            f.write(repo_json)


    def document(self):
        index = self.build_index()
        with open('templates/readme/1.j2','r') as f:
            temp = f.read()
        prompt = self.prompt+"```\n"+temp+"\n```"
        response = self.contextbot(index=index, input_text=prompt)
        response+="\n\n:wink: _This **README.md** was created with [Docify](https://github.com/iamadhee/docify)_"

        with open('docify_readme.md', 'w') as f:
            f.write(response)

    def debug(self):
        index = self.build_index(save=True)
        while True:
            pt = input('ask: ')
            print(self.contextbot(index=index, input_text=pt))


if __name__=='__main__':
    import sys
    API_KEY = sys.argv[1]
    model_llm = OpenAI(api_key=API_KEY, model='gpt-3.5-turbo')
    docuter = ReadmeGen()
    docuter.debug()
