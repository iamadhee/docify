import openai
import subprocess
from pathlib import Path
from tqdm import tqdm
import yaml

with open('config.yaml','rb') as f:
    config = yaml.safe_load(f)

AI_MODE = config['AI_MODE'].title()
MODEL = config['MODEL']

class Docify:

    def __init__(self, api_key) -> None:
        openai.api_key = api_key
        self.model = MODEL
        self.messages = [{'role':'system', \
                          'content':f'You are an AI specialized in {AI_MODE}. Do not answer anything other than {AI_MODE}-related queries.'}, \
                         {'role':'assistant', \
                          'content':f'Understood! I am here to help with {AI_MODE}-related queries. Please feel free to ask any related questions you might have.'}, \
                        ]
        self.tree_prompt = "This is my repository's folder structure from the root folder: \n"
        self.file_prompt = "Below is the content of {file_name}: \n ```{file_content}```"  
        self.doc_prompt = "Now create a README.md for the whole repository, based on the file contents and folder structure I just provided"
        self.cur_path = Path()

    def chatbot(self, input:str) -> None:
        if input:
            self.messages.append({'role': 'user', 'content': input})
            chat = openai.ChatCompletion.create(
                model=self.model, \
                messages=self.messages, \
            )
            reply=chat.choices[0].message.content
            self.messages.append({'role':'assistant','content':reply})

    def build_tree(self,prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """    
        space =  '    '
        branch = '│   '
        tee =    '├── '
        last =   '└── '
        contents =  self.get_file_list()
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
    
    def get_file_list(self, return_only_files:bool=False) -> list: 
        files = list(filter(
                            lambda path: not any((part for part in path.parts if part.startswith("."))), \
                            self.cur_path.rglob("*")
                           ))
        if return_only_files:
            files = [file for file in files if file.is_file()]
        return files
    
    def document(self, write:bool=False) -> str:
        files = self.get_file_list(return_only_files=True)
        tree = self.get_tree()
        self.chatbot(self.tree_prompt+tree)

        for file in tqdm(files):
            with open(file,'r') as f:
                file_content = f.read()
                prompt = self.file_prompt.format(file_name=str(file), file_content=file_content)
                self.chatbot(prompt)

        self.chatbot(self.doc_prompt)
        response = self.messages[-1]['content']
        
        if write:
            with open('README.md','w') as f:
                f.write(response)
            return "written the documentation to README.md"
        else:
            with open('docify.md','w') as f:
                f.write(response)
            return "written the documentation to docify.md"
        

