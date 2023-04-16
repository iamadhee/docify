from gpt_index import SimpleDirectoryReader, JSONReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from pathlib import Path
import json


class Docify:
     
    def __init__(self): 
        self.cur_path = Path()
        
    def build_prompt_helper(self, max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit) :
        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        return prompt_helper
    
    def build_llm_predictor(self, llm):
        llm_predictor = LLMPredictor(llm=llm)
        return llm_predictor
    
    def load_data_from_path(self, directory_path):
        documents = SimpleDirectoryReader(directory_path, recursive=True).load_data()
        return documents

    def construct_index(self, documents, llm_predictor, prompt_helper):
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        return index
    
    def chatbot(self, index, input_text):
        response = index.query(input_text)
        return response.response
    
    def get_file_list(self, path, return_only_files:bool=False) -> list: 
        files = list(filter(
                            lambda path: not any((part for part in path.parts if part.startswith("."))), \
                            path.rglob("*")
                           ))
        if return_only_files:
            files = [file for file in files if file.is_file()]
        return files
    
    def build_tree(self, dir_path, prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """    
        # import pdb; pdb.set_trace()
        space =  '    '
        branch = '│   '
        tee =    '├── '
        last =   '└── '
        contents =  self.get_file_list(dir_path)
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir(): # extend the prefix and recurse:
                extension = branch if pointer == tee else space 
                # i.e. space because last, └── , above so no more |
                yield from self.build_tree(path, prefix=prefix+extension)

    def get_tree(self) -> str:
        tree_str = "\n".join(self.build_tree(self.cur_path))
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
                        # print(entry)
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
        with open('docify_index.json','w') as f:
            f.write(repo_json)

    def load_data_from_json(self):
        self.create_index_json()
        documents = JSONReader().load_data('docify_index.json')
        Path('docify_index.json').unlink()
        return documents

    def document(self):
        num_outputs = 512
        prompt_helper = self.build_prompt_helper(max_input_size = 4096,
                                                num_outputs=num_outputs,
                                                max_chunk_overlap = 20,
                                                chunk_size_limit = 600)
       
        llm_predictor = self.build_llm_predictor(ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
        documents = self.load_data_from_json()
        index = self.construct_index(documents=documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        ques = "Give me a long, fun and instagram style content for a README.md file for this repository, with the context of the contents and folder structure of the repository and also by interrelating the contents of each file and what each file does. Don't explain the code in the description. Give the content in raw markdown format."
        context = None

        if context:
            ques = ques + '\n' + context
        # import pdb; pdb.set_trace()
        response = self.chatbot(index=index,input_text=ques)

        with open('dummy.md','w') as f:
            f.write(response)

yo = Docify()
yo.document()



