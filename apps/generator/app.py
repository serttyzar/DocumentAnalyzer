import os
from args_parser import ArgsParser
from doc_generator import generate_multiple_documents

def main():
    args = ArgsParser()
   
    os.makedirs(args.output, exist_ok=True)
    generate_multiple_documents(args.count, args.output)
    
if __name__ == "__main__":
    main()