# import fitz
# import os

# pdf = fitz.open("sports_guide_with_images.pdf")
# os.makedirs("images", exist_ok=True)

# page = pdf[0]

# image_list = page.get_images(full=True)
# print(image_list)
# first_img = image_list[0]
# xref = first_img[0]

# base_image = pdf.extract_image(xref)

# print(base_image.keys())
# print(base_image["ext"])
# print(f"type {type(base_image["image"])}")
# print(len(base_image["image"]))
# # image bytes

# image_bytes = base_image["image"]   # actual image data
# image_ext = base_image["ext"]       # png / jpeg etc.


# print(image_bytes)
# print(image_ext)
# # image_path = f"images/page_1_img_1.{image_ext}"

# # with open(image_path, "wb") as f:
# #     f.write(image_bytes)

# # print("Saved:", image_path)

# # print(xref)
# # for page_no in range(len(pdf)):
# #     page = pdf[page_no]
# #     images = page.get_images(full=True)

# #     print(f"Page {page_no + 1} has {len(images)} image(s)")

# #     for img_index, img in enumerate(images, start=1):
# #         xref = img[0]   
# #         base_image = pdf.extract_image(xref)

# #         image_bytes = base_image["image"]   # actual image data
# #         image_ext = base_image["ext"]       # png / jpeg etc.

# #         image_path = f"images/page_{page_no+1}_img_{img_index}.{image_ext}"

# #         with open(image_path, "wb") as f:
# #             f.write(image_bytes)

# #         print("Saved:", image_path)




from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader

loader = DirectoryLoader(
    path="pdfs",
    glob="*.pdf",
    recursive=True,
    loader_cls=PyMuPDFLoader,
    loader_kwargs={
        "extract_images_in_pdf": True,
    }
)

docs = loader.load()
print(len(docs))