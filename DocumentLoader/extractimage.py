import os
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredPDFLoader

load_dotenv()

# Define where you want to save the extracted images
IMAGE_DIR = "images_folder"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# 1. Initialize the Unstructured PDF Loader with extraction settings
# We tell unstructured to physically extract the images and save them to our folder automatically.
# 1. Initialize the Unstructured PDF Loader with specific backend overrides
loader = UnstructuredPDFLoader(
    "sports_images_gallery.pdf",
    strategy="hi_res",
    mode="elements",
    extract_images_in_pdf=True
)

print("Loading and partitioning PDF using hi_res strategy... (Extracting images simultaneously)")
documents = loader.load()
print(f"Successfully split the document into {len(documents)} structural elements.\n")

# 2. Iterate through elements to process text and detect images
image_elements_count = 0
table_elements_count = 0

for idx, doc in enumerate(documents):
    element_type = doc.metadata.get("category", "Unknown")
    page_number = doc.metadata.get("page_number", 1)
    
    # Check if the element represents an image chunk
    if element_type == "Image":
        image_elements_count += 1
        print(f"--- [Element {idx} | Page {page_number}] Found an IMAGE ---")
        
        # Unstructured automatically names and saves extracted images into IMAGE_DIR.
        # You can see the file name inside the metadata dictionary.
        filename = doc.metadata.get("filename")
        print(f"Image physically extracted and saved inside the {IMAGE_DIR} directory.")
        
        # Check if Tesseract read any text inside that image
        if doc.page_content.strip():
            print(f"Extracted Text from Image via OCR: {doc.page_content.strip()}")
        else:
            print("Visual image detected (No text found inside it).")
        print("-" * 40)
        
    elif element_type == "Table":
        table_elements_count += 1
        print(f"--- [Element {idx} | Page {page_number}] Found a TABLE ---")
        print(doc.page_content.strip())
        print("-" * 40)

print("\n================ SUMMARY ================")
print(f"Total structural elements parsed: {len(documents)}")
print(f"Total Image elements extracted: {image_elements_count}")
print(f"Total Table elements detected: {table_elements_count}")