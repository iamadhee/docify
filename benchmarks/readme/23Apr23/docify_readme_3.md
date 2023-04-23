PROMPT_3: "You are an expert in generating README.md files for repositories. Fill up the below fields with fun content for the repo named {0}. Add styling to make the README file look eye catching.\n"

<h1 align="center">Docify</h1>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
</p>

## What is Docify?

Docify is a Python package that allows you to easily generate README.md files for your repositories using GPT models.

## Features

- Generate high-quality README.md files using GPT models
- Customize the look and feel of your README.md file with templates
- Support for multiple GPT models for text generation

## How Docify Works

Docify reads a configuration file and uses GPT models to generate text for your README.md file. You can customize the templates used to generate the file and choose from multiple GPT models for text generation.

## Getting Started

To get started with Docify, simply install the package using pip:

```
pip install docify
```

Next, create a configuration file for your repository in YAML format:

```yaml
model: gpt-3
prompt: |
  # My Awesome Repository

  This repository contains some awesome code that does amazing things. In this README.md file, we'll cover what the repository is, its features, how it works, getting started with it, contributing to it, its license, and some concluding remarks.

  ## What is My Awesome Repository?

  ...

template: templates/readme/1.j2
files:
  - config.yaml
  - documentor.py
  - models/base_model.py
  - models/openai_complete.py
  - requirements.txt
  - templates/readme/1.j2
  - tests/test.py
  - LICENSE
```

Finally, run the following command to generate your README.md file:

```
docify generate
```

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Conclusion

Thanks for checking out Docify! We hope it makes generating README.md files a breeze for you. If you have any questions, comments, or feedback, please don't hesitate to get in touch with us.

:wink: _This **README.md** was created with [Docify](https://github.com/iamadhee/docify)_