
import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="docify",
    version="0.0.1",
    author="Adheeban Manoharan",
    author_email="caeser.alfred@gmail.com",
    description=("A documentation tool that leverages ChatGPT to produce a comprehensive README.md for your repository based on the context of content in it"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamadhee/docify",
    project_urls={
        "Bug Tracker": "https://github.com/iamadhee/docify/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests","openai","tqdm","pathlib","pyyaml"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "docify = docify.cli:main",
        ]
    }
)

