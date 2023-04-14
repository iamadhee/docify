#! /usr/bin/env python
"""
The command-line interface for the docfiy tool
"""
import argparse
from documentor import Docify

def main():
    parser = argparse.ArgumentParser(
        description="A documentation tool that leverages ChatGPT to produce a comprehensive README.md for your repository based on the context of content in it."
    )

    parser.add_argument(
        "api_key", type=str,
        help="The OpenAI API Key"
    )

    parser.add_argument(
        "--write -w", type=str,
        choices=['true', 'false'],
        help="Whether to write the model's output to README.md or not, if set to False: the output will be written to docify.md file instead"
    )
    
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    args = parser.parse_args()
    docify = Docify(args.api_key)
    out_message = docify.document(write=str2bool(args.write))
    print(out_message)

if __name__ == "__main__":
    main()