# Docify

Hate documenting your code repo? Well, that makes the two of us. Fear not! ChatGPT is here to save us. Docify is a command-line tool that generates documentation for your repository using ChatGPT. It uses OpenAI's GPT-3 model to provide a conversational experience and create a README.md file based on the content of files and the folder structure of your repository.

---

# Usage

To use Docify, follow these steps:

## Install Docify using pip:

`pip install docify`

Run Docify at the root folder of your repository, providing your API key as an argument:

`docify <API_KEY>`

**Note**: Replace <API_KEY> with your actual OpenAI API key. Here's [how to generate one](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).

Docify will analyze the folder structure of your repository and the content of your files. It will have a conversational chat with the ChatGPT model, discussing the contents and structure of your repository.

Finally, Docify will create a README.md file with the generated documentation. You can choose to write the documentation to README.md or docify.md by specifying the write flag. When set to True, Docify will write the generated documentation to README.md of the repository, and in the docify.md, if set to False. Default value for the write flag is False.

----

# Documentation

The documentation is generated based on the following steps:

* Analyzing the folder structure: Docify generates a visual tree structure of your repository's folder hierarchy, displaying the directory names and file names, 

* Analyzing file contents: Docify (ChatGPT) reads the content of each file in your repository and includes it in the documentation as code blocks.

* Generating README.md: Docify creates a README.md file with the generated documentation, summarizing the contents and structure of your repository, with context we gave to the model.

----

:wink: _This **README.md** was created with Docify_ 
