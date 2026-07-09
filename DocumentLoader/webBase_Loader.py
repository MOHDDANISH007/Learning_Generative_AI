from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
     web_paths=[
        "https://huggingface.co/empero-ai/Qwythos-9B-Claude-Mythos-5-1M-GGUF"
    ],
    requests_per_second=20,
    default_parser="html.parser",
    raise_for_status=True,
    continue_on_failure=True,
    show_progress=True
)

docs = loader.load()



print("Total docs:", len(docs))

for i, doc in enumerate(docs, start=1):
    print(f"\n========== DOC {i} ==========")
    print(doc.page_content[:1500])
    print(doc.metadata)