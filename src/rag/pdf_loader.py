# Loads text from PDF files while keeping source and page information.
# Loads all PDF files from a folder and preserves their metadata.
# Splits text into smaller chunks with overlap between consecutive chunks.
# Creates chunks while keeping the original source and page information.
# Displays the total number of chunks and information from the first chunk.


from pathlib import Path
from pypdf import PdfReader


# Defines a function called load_pdf that receives one PDF file path.
def load_pdf(file_path):

    # Creates a PDF reader object and opens the specified PDF file.
    reader = PdfReader(file_path)

    # Creates an empty list where extracted pages will be stored.
    pages = []

    # Loops through every page in the PDF and starts counting pages from 1.
    for page_number, page in enumerate(reader.pages, start=1):

        # Extracts the text content from the current PDF page.
        page_text = page.extract_text()

        # Checks if text was successfully extracted from the page.
        if page_text:

            # Adds the page text and its metadata to the pages list.
            pages.append({

                # Stores the extracted text from the current page.
                "text": page_text,

                # Stores the name of the PDF file as the source.
                "source": Path(file_path).name,

                # Stores the current page number.
                "page": page_number
            })

    # Returns the list containing the extracted pages and their metadata.
    return pages


# Defines a function that loads all PDF files from a folder and preserves metadata.
def load_all_pdfs(folder_path):

    # Creates an empty list where all extracted pages will be stored.
    all_pages = []

    # Searches for all files with the .pdf extension inside the folder.
    pdf_files = Path(folder_path).glob("*.pdf")

    # Loops through each PDF file found in the folder.
    for pdf_file in pdf_files:

        # Prints the name of the PDF file currently being processed.
        print(f"Reading: {pdf_file.name}")

        # Calls load_pdf() to extract the pages from the current PDF file.
        pages = load_pdf(pdf_file)

        # Adds all extracted pages to the complete pages list.
        all_pages.extend(pages)

    # Returns all extracted pages with their metadata.
    return all_pages


# Defines a function that splits text into smaller chunks with overlap.
def split_text(text, chunk_size=500, overlap=100):

    # Splits the complete text into a list of individual words.
    words = text.split()

    # Creates an empty list where text chunks will be stored.
    chunks = []

    # Sets the starting position for the first chunk.
    start = 0

    # Loops while there are still words available to process.
    while start < len(words):

        # Calculates the ending position of the current chunk.
        end = start + chunk_size

        # Selects the words for the current chunk and joins them into one string.
        chunk = " ".join(words[start:end])

        # Adds the created chunk to the chunks list.
        chunks.append(chunk)

        # Moves the starting position forward while keeping the defined overlap.
        start += chunk_size - overlap

    # Returns the list containing all generated chunks.
    return chunks


# Defines a function that creates chunks while preserving source and page metadata.
def create_chunks(pages, chunk_size=500, overlap=100):

    # Creates an empty list where all chunks will be stored.
    chunks = []

    # Loops through each page containing extracted text and metadata.
    for page in pages:

        # Splits the current page text into smaller chunks.
        page_chunks = split_text(
            page["text"],
            chunk_size,
            overlap
        )

        # Loops through each chunk created from the current page.
        for chunk in page_chunks:

            # Adds the chunk and its original metadata to the chunks list.
            chunks.append({

                # Stores the text content of the current chunk.
                "text": chunk,

                # Stores the name of the original PDF file.
                "source": page["source"],

                # Stores the page number where the chunk came from.
                "page": page["page"]
            })

    # Returns all generated chunks with their source and page metadata.
    return chunks


# Checks if this file is being executed directly.
if __name__ == "__main__":

    # Defines the folder containing the PDF documents.
    documents_folder = "documents"

    # Step 1: Loads all PDF pages while preserving their metadata.
    pages = load_all_pdfs(documents_folder)

    # Step 2: Creates chunks while preserving source and page metadata.
    chunks = create_chunks(pages)

    # Prints a separator line for better output formatting.
    print("\n------------------------")

    # Displays the total number of generated chunks.
    print(f"Total chunks: {len(chunks)}")

    # Prints another separator line.
    print("------------------------")

    # Checks if the chunks list contains at least one element.
    if chunks:

        # Prints a title before showing the first chunk.
        print("\nFirst chunk:\n")

        # Displays the text content of the first generated chunk.
        print(chunks[0]["text"])

        # Prints a title before showing the source of the first chunk.
        print("\nSource:")

        # Displays the PDF file name where the first chunk came from.
        print(chunks[0]["source"])

        # Prints a title before showing the page number of the first chunk.
        print("\nPage:")

        # Displays the page number where the first chunk came from.
        print(chunks[0]["page"])