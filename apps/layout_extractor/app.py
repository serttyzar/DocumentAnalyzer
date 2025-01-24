import os
from args_parser import ArgsParser
from pdf_utils.pdf_layout_extractor import PDFLayoutExtractor

def main():
    args = ArgsParser()

    os.makedirs(args.visualization_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    
    extractor = PDFLayoutExtractor(file_path=args.input, output_dir=args.output_dir, visualize_dir=args.visualization_dir)
    extractor.extract_layout()

    extractor.visualize_pages(args.pages_to_visualize)
    extractor.close_document()

if __name__ == "__main__":
    main()
