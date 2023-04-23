<div align="center">
<img width="200px" src="https://raw.githubusercontent.com/iamadhee/docify/main/assets/logo.png">
<h1>Docify</h1></div>

<div align="center">
Hate documenting your code? Fear not! ChatGPT powered Docify is here to save the day!
</div>

## What is Docify?

Docify is a Python-based documentation tool that simplifies the documentation process for developers. It allows you to generate documentation for your codebase, including functions, classes, and modules. With Docify, you can easily create a comprehensive documentation website for your project. 

----

## Features

- Automatic generation of documentation for your codebase

----

## How Docify Works

Docify uses the OpenAI GPT-3 API to generate documentation for your codebase. It analyzes your code and generates a summary of each function, class, and module. It then uses natural language processing to generate a description of each item, including its purpose and usage. 

---

## Getting Started
Just copy the `documentor.py`, `requirements.txt` and `config.yaml` files from the Docify's repository and paste it into the root folder of the repository you want to document. That's it! You are good to go. Everything else is already configured. 

Run ```pip3 install -r requirements.txt``` to install all the dependencies.

After that, at your root folder just run, ```python3 documentor.py <API_KEY>```

You need to have a OpenAI API key, to run docify. Don't have a key? Here's [how to get one](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/). Upon successful run of the said command, you'd have a file created named `docify_readme.md`. After careful review, paste the contents into your repository's README.md file. That's it, you are done with your documentation !

If you feel adventurous, try fiddling a bit with the prompt and the models in the `config.yaml` file. You might get a better documentation.

> **Warning**
>
> This tool shares the contents (codes) in your repository to make GPT-3 understand your repository. Please exercise caution while using the tool.

----

## Contributing

We welcome contributions to the Docify project. If you find a bug or have a feature request, please submit an issue on GitHub. If you would like to contribute code to the project, please submit a pull request. Your suggestions are always welcome !

----

## License

Docify is licensed under the MIT License. See the `LICENSE` file for more information.

----

## Conclusion

We hope you find Docify to be a useful tool for documenting your code. With its intuitive interface and powerful features

:wink: _This **README.md** was created with [Docify](https://github.com/iamadhee/docify) (Didn't change a thing! Well.. Except pasting the logo)_