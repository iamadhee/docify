import openai
import subprocess
from pathlib import Path

class Docify:

    def __init__(self) -> None:
        openai.api_key = "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"
        self.model = 'gpt-3.5-turbo'
        self.messages = [{'role':'system', \
                          'content':'You are an AI specialized in Code. Do not answer anything other than code-related queries.'}, \
                         {'role':'assistant', \
                          'content':'Understood! I am here to help with code-related queries. Please feel free to ask any coding questions you have.'}, \
                        ]
        self.tree_prompt = "This is my repository's folder structure from the root folder: \n"
        self.file_prompt = "Below is the content of {file_name}: \n ```{file_content}```"  
        self.doc_prompt = "Now create a README.md for the whole repository, based on the file contents and folder structure I just provided"
        self.cur_path = Path()

    def chatbot(self, input):
        if input:
            self.messages.append({'role': 'user', 'content': input})
            chat = openai.ChatCompletion.create(
                model=self.model, \
                messages=self.messages, \
            )
            reply=chat.choices[0].content
            self.messages.append({'role':'assistant','content':reply})

    def build_tree(self,dir_path,prefix: str=''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters
        """    
        space =  '    '
        branch = '│   '
        tee =    '├── '
        last =   '└── '
        contents =  list(filter(
                            lambda path: not any((part for part in path.parts if part.startswith("."))), \
                            dir_path.rglob("*")
                           ))
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir(): # extend the prefix and recurse:
                extension = branch if pointer == tee else space 
                # i.e. space because last, └── , above so no more |
                yield from self.build_tree(path, prefix=prefix+extension)

    def get_tree(self):
        tree_str = '\n'.join(self.build_tree(self.cur_path))
        return tree_str
    
    def get_file_list(self): 
        all_files = self.cur_path.rglob('*')
        files = [file for file in all_files if file.is_file()]
        return files
    
    def document(self):
        files = self.get_file_list()
        tree = self.get_tree()
        self.chatbot(self.tree_prompt+tree)

        for file in files:
            with open(file,'r') as f:
                file_content = f.read()
                prompt = self.file_prompt.format(file_name=str(file), file_content=file_content)
                self.chatbot(prompt)

        response = self.chatbot(self.doc_prompt)

        with open('README.md','w') as f:
            f.write(response)
        

doc = Docify()
doc.get_tree()

