

# Defines a function called load_pdf that receives one PDF file path.

# Defines a function that loads all PDF files from a folder.

# Defines a function that splits a large text into smaller chunks.

# Checks if this file is being executed directly.

from pathlib import Path
from pypdf import PdfReader


# Defines a function called load_pdf that receives one PDF file path.
def load_pdf(file_path):

    # Creates an empty string that will store the extracted PDF text.
    text = ""

    # Creates a PDF reader object and opens the specified PDF file.
    reader = PdfReader(file_path)

    # Loops through every page inside the PDF document.
    for page in reader.pages:

        # Extracts the text content from the current PDF page.
        page_text = page.extract_text()

        # Checks if text was successfully extracted from the page.
        if page_text:

            # Adds the extracted page text to the complete text variable.
            # The "\n" creates a new line after each page.
            text += page_text + "\n"

    # Returns the complete extracted text from the PDF file.
    return text



# Defines a function that loads all PDF files from a folder.
def load_all_pdfs(folder_path):

    # Creates an empty string to store text from all PDF files.
    all_text = ""

    # Searches for all files with the .pdf extension inside the folder.
    pdf_files = Path(folder_path).glob("*.pdf")

    # Loops through each PDF file found in the folder.
    for pdf_file in pdf_files:

        # Prints the name of the PDF file currently being processed.
        print(f"Reading: {pdf_file.name}")

        # Calls load_pdf() to extract text from the current PDF file.
        pdf_text = load_pdf(pdf_file)

        # Adds the extracted PDF text to the complete text variable.
        all_text += pdf_text + "\n"

    # Returns the combined text from all PDF documents.
    return all_text



# Defines a function that splits a large text into smaller chunks.
def split_text(text, chunk_size=500):

    # Splits the complete text into a list of individual words.
    words = text.split()

    # Creates an empty list where text chunks will be stored.
    chunks = []

    # Loops through the words list using the defined chunk size.
    for i in range(0, len(words), chunk_size):

        # Selects a group of words and joins them into a single string.
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        # Adds the created chunk to the chunks list.
        chunks.append(chunk)

    # Returns the list containing all generated chunks.
    return chunks



# Checks if this file is being executed directly.
if __name__ == "__main__":

    # Defines the folder containing the PDF documents.
    documents_folder = "documents"

    # Step 1: Loads all PDF files and extracts their text.
    content = load_all_pdfs(documents_folder)

    # Step 2: Splits the extracted text into smaller chunks.
    chunks = split_text(content)

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

        # Displays the first generated text chunk.
        print(chunks[0])






# Defines a function called load_pdf that receives one PDF file path.
    # Creates an empty string that will store the extracted PDF text.
    # Creates a PDF reader object and opens the specified PDF file.
    # Loops through every page inside the PDF document.
        # Extracts the text content from the current PDF page.
        # Checks if text was successfully extracted from the page.
            # Adds the extracted page text to the complete text variable.
            # The "\n" creates a new line after each page.
    # Returns the complete extracted text from the PDF file.

# Defines a function that loads all PDF files from a folder.
    # Creates an empty string to store text from all PDF files.
    # Searches for all files with the .pdf extension inside the folder.
    # Loops through each PDF file found in the folder.
        # Prints the name of the PDF file currently being processed.
        # Calls load_pdf() to extract text from the current PDF file.
        # Adds the extracted PDF text to the complete text variable.
    # Returns the combined text from all PDF documents.

# Defines a function that splits a large text into smaller chunks.
    # Splits the complete text into a list of individual words.
    # Creates an empty list where text chunks will be stored.
    # Loops through the words list using the defined chunk size.
        # Selects a group of words and joins them into a single string.
        # Adds the created chunk to the chunks list.
    # Returns the list containing all generated chunks.

# Checks if this file is being executed directly.
    # Defines the folder containing the PDF documents.
    # Step 1: Loads all PDF files and extracts their text.
    # Step 2: Splits the extracted text into smaller chunks.
    # Prints a separator line for better output formatting.
    # Displays the total number of generated chunks.
    # Prints another separator line.
    # Checks if the chunks list contains at least one element.
        # Prints a title before showing the first chunk.
        # Displays the first generated text chunk.