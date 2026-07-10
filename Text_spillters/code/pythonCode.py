"""
DOCUMENT STRUCTURE & PROCESSING EDUCATIONAL EXAMPLE
==================================================
This shows how Markdown/HTML documents are processed in LangChain-style systems.
Run this to see how document structure works programmatically.
"""

import os
import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

# ============================================================
# PART 1: DOCUMENT MODELS - Understanding Structure
# ============================================================

@dataclass
class Document:
    """Represents a document with content and metadata."""
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(self.content.encode()).hexdigest()[:8]
    
    def get_heading_structure(self) -> List[Dict[str, str]]:
        """Extract heading structure from markdown content."""
        headings = []
        lines = self.content.split('\n')
        
        for line in lines:
            # Match markdown headings (#, ##, ###, etc.)
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append({
                    'level': level,
                    'title': title,
                    'id': self._generate_id(title)
                })
        
        return headings
    
    def get_links(self) -> List[Dict[str, str]]:
        """Extract all links from the document."""
        links = []
        
        # Markdown links: [text](url)
        md_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', self.content)
        for text, url in md_links:
            links.append({
                'type': 'markdown',
                'text': text,
                'url': url,
                'is_internal': url.startswith('#') or not url.startswith('http')
            })
        
        # HTML links: <a href="url">text</a>
        html_links = re.findall(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', self.content)
        for url, text in html_links:
            links.append({
                'type': 'html',
                'text': text.strip(),
                'url': url,
                'is_internal': url.startswith('#') or not url.startswith('http')
            })
        
        return links
    
    def get_structure_summary(self) -> Dict[str, Any]:
        """Get a complete structure summary."""
        return {
            'id': self.id,
            'content_length': len(self.content),
            'word_count': len(self.content.split()),
            'heading_count': len(self.get_heading_structure()),
            'link_count': len(self.get_links()),
            'headings': self.get_heading_structure(),
            'links': self.get_links(),
            'metadata': self.metadata
        }
    
    @staticmethod
    def _generate_id(text: str) -> str:
        """Generate an ID from text (like GitHub does)."""
        # Convert to lowercase, replace spaces with hyphens, remove special chars
        return re.sub(r'[^a-z0-9-]', '', text.lower().replace(' ', '-'))

@dataclass
class DocumentCollection:
    """Manages a collection of related documents."""
    documents: List[Document] = field(default_factory=list)
    
    def add_document(self, doc: Document):
        self.documents.append(doc)
    
    def find_document_by_id(self, doc_id: str) -> Optional[Document]:
        for doc in self.documents:
            if doc.id == doc_id:
                return doc
        return None
    
    def get_all_headings(self) -> List[Dict[str, Any]]:
        """Get all headings from all documents."""
        all_headings = []
        for doc in self.documents:
            for heading in doc.get_heading_structure():
                all_headings.append({
                    'document_id': doc.id,
                    'level': heading['level'],
                    'title': heading['title'],
                    'id': heading['id']
                })
        return all_headings
    
    def get_all_links(self) -> List[Dict[str, Any]]:
        """Get all links from all documents."""
        all_links = []
        for doc in self.documents:
            for link in doc.get_links():
                all_links.append({
                    'document_id': doc.id,
                    **link
                })
        return all_links
    
    def create_document_graph(self) -> Dict[str, Any]:
        """Create a graph showing how documents link to each other."""
        graph = {
            'nodes': [],
            'edges': []
        }
        
        # Add all documents as nodes
        for doc in self.documents:
            graph['nodes'].append({
                'id': doc.id,
                'metadata': doc.metadata,
                'heading_count': len(doc.get_heading_structure())
            })
        
        # Add links as edges
        for link in self.get_all_links():
            if link['is_internal']:
                graph['edges'].append({
                    'from': link['document_id'],
                    'to': link['url'].replace('#', '').strip('/'),
                    'text': link['text']
                })
        
        return graph

# ============================================================
# PART 2: DOCUMENT PROCESSORS - Converting & Processing
# ============================================================

class DocumentProcessor:
    """Handles document processing and transformation."""
    
    @staticmethod
    def markdown_to_html(markdown_content: str) -> str:
        """Convert Markdown to HTML (simplified conversion for learning)."""
        html = markdown_content
        
        # Headings
        for i in range(1, 7):
            html = re.sub(
                rf'^{"#" * i}\s+(.+)$',
                rf'<h{i}>\1</h{i}>',
                html,
                flags=re.MULTILINE
            )
        
        # Bold
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        
        # Italic
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
        
        # Links: [text](url)
        html = re.sub(
            r'\[([^\]]+)\]\(([^\)]+)\)',
            r'<a href="\2">\1</a>',
            html
        )
        
        # Images: ![alt](src)
        html = re.sub(
            r'!\[([^\]]+)\]\(([^\)]+)\)',
            r'<img src="\2" alt="\1">',
            html
        )
        
        # Lists - unordered
        html = re.sub(
            r'^-\s+(.+)$',
            r'<li>\1</li>',
            html,
            flags=re.MULTILINE
        )
        html = re.sub(
            r'(<li>.*?</li>\n)+',
            r'<ul>\n\g<0></ul>\n',
            html,
            flags=re.DOTALL
        )
        
        # Lists - ordered
        html = re.sub(
            r'^\d+\.\s+(.+)$',
            r'<li>\1</li>',
            html,
            flags=re.MULTILINE
        )
        html = re.sub(
            r'(<li>.*?</li>\n)+',
            r'<ol>\n\g<0></ol>\n',
            html,
            flags=re.DOTALL
        )
        
        # Paragraphs (basic)
        html = re.sub(
            r'^(?!<[hlu]|<)/?([^<].+)$',
            r'<p>\1</p>',
            html,
            flags=re.MULTILINE
        )
        
        return html
    
    @staticmethod
    def extract_sections(document: Document, min_words: int = 50) -> List[Document]:
        """Split document into sections based on headings."""
        sections = []
        lines = document.content.split('\n')
        current_section = []
        current_heading = "Introduction"
        section_counter = 1
        
        for line in lines:
            # Check if it's a heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if heading_match:
                # Save previous section if it has content
                if current_section:
                    section_content = '\n'.join(current_section)
                    if len(section_content.split()) >= min_words:
                        sections.append(Document(
                            content=section_content,
                            metadata={
                                'section_title': current_heading,
                                'section_number': section_counter,
                                'parent_document': document.id
                            }
                        ))
                        section_counter += 1
                
                # Start new section
                current_heading = heading_match.group(2).strip()
                current_section = [line]
            else:
                current_section.append(line)
        
        # Save final section
        if current_section:
            section_content = '\n'.join(current_section)
            if len(section_content.split()) >= min_words:
                sections.append(Document(
                    content=section_content,
                    metadata={
                        'section_title': current_heading,
                        'section_number': section_counter,
                        'parent_document': document.id
                    }
                ))
        
        return sections
    
    @staticmethod
    def create_embeddings_text(document: Document) -> str:
        """Create text for embeddings (includes structure info)."""
        headings = document.get_heading_structure()
        heading_text = ' '.join([h['title'] for h in headings])
        
        return f"""
        Document ID: {document.id}
        Structure: {heading_text}
        Content: {document.content[:500]}...
        """

# ============================================================
# PART 3: DOCUMENT LOADERS - Loading from different sources
# ============================================================

class DocumentLoader:
    """Load documents from various sources."""
    
    @staticmethod
    def load_markdown_from_string(content: str, filename: str = "untitled.md") -> Document:
        """Load a document from a markdown string."""
        return Document(
            content=content,
            metadata={
                'source': filename,
                'type': 'markdown',
                'loaded_at': datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def load_markdown_from_file(filepath: str) -> Document:
        """Load a document from a markdown file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Document(
            content=content,
            metadata={
                'source': filepath,
                'type': 'markdown',
                'loaded_at': datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def load_sample_documents() -> DocumentCollection:
        """Load sample documents for educational purposes."""
        collection = DocumentCollection()
        
        # Document 1: Guide to Document Structure
        doc1_content = """
# Complete Guide to Document Structure
## Understanding Markdown and HTML
### Introduction
Document structure is fundamental to organizing information. Whether you're writing documentation, building a website, or creating content for a RAG system, understanding structure matters.

### Key Concepts
#### Headings
Headings create hierarchy. In Markdown, we use # for H1, ## for H2, etc. In HTML, these become <h1>, <h2>, etc.

#### Links
Links connect documents. [Internal links](#section) use anchors. [External links](https://example.com) use full URLs.

### Practical Example
Here's a practical example:
- Use consistent heading levels
- Add descriptive link text
- Test all links regularly
"""
        
        doc1 = DocumentLoader.load_markdown_from_string(doc1_content, "structure_guide.md")
        collection.add_document(doc1)
        
        # Document 2: LangChain Integration
        doc2_content = """
# LangChain and Document Structure
## Why Structure Matters for RAG
### Retrieval-Augmented Generation
RAG systems need structured documents to work effectively. Headings, sections, and links all provide context.

### Document Loaders
LangChain supports various document loaders:
- TextLoader: Load plain text
- UnstructuredMarkdownLoader: Load markdown with structure
- CSVLoader: Load tabular data

### Practical Integration
When building RAG systems:
1. Load documents with structure preserved
2. Split by sections using headings
3. Create embeddings with structural context
4. Retrieve based on semantic similarity
"""
        
        doc2 = DocumentLoader.load_markdown_from_string(doc2_content, "langchain_integration.md")
        collection.add_document(doc2)
        
        # Document 3: Advanced Linking
        doc3_content = """
# Advanced Document Linking
## Cross-Reference Patterns
### Internal References
[See structure guide](#structure-guide)
[Check LangChain docs](#langchain-documentation)

### External Resources
- [Markdown Guide](https://www.markdownguide.org)
- [HTML Specification](https://html.spec.whatwg.org)
- [LangChain Docs](https://python.langchain.com)

### Navigation Structure
Create a navigation system:
- Home → [Structure Guide](structure_guide.md)
- Guide → [LangChain](langchain_integration.md)
- Reference → [Advanced Topics](#advanced)
"""
        
        doc3 = DocumentLoader.load_markdown_from_string(doc3_content, "advanced_linking.md")
        collection.add_document(doc3)
        
        return collection

# ============================================================
# PART 4: MAIN DEMONSTRATION
# ============================================================

def demonstrate_document_processing():
    """Main demonstration showing how document structure works."""
    
    print("=" * 60)
    print("📚 DOCUMENT STRUCTURE PROCESSING DEMONSTRATION")
    print("=" * 60)
    print("\nThis demonstrates how Markdown/HTML documents are processed")
    print("in LangChain-style document systems.\n")
    
    # Step 1: Load documents
    print("STEP 1: LOADING DOCUMENTS")
    print("-" * 40)
    collection = DocumentLoader.load_sample_documents()
    print(f"✅ Loaded {len(collection.documents)} documents")
    
    # Step 2: Examine each document's structure
    print("\nSTEP 2: EXAMINING DOCUMENT STRUCTURE")
    print("-" * 40)
    
    for doc in collection.documents:
        print(f"\n📄 Document: {doc.metadata.get('source', 'Unknown')}")
        print(f"   ID: {doc.id}")
        print(f"   Length: {len(doc.content)} characters")
        print(f"   Words: {len(doc.content.split())}")
        
        headings = doc.get_heading_structure()
        print(f"   Headings: {len(headings)}")
        for h in headings:
            print(f"      {'  ' * (h['level'] - 1)}H{h['level']}: {h['title']} (ID: {h['id']})")
        
        links = doc.get_links()
        print(f"   Links: {len(links)}")
        for link in links:
            type_icon = "🔗" if link['is_internal'] else "🌐"
            print(f"      {type_icon} {link['text']} → {link['url']}")
    
    # Step 3: Convert Markdown to HTML
    print("\nSTEP 3: MARKDOWN → HTML CONVERSION")
    print("-" * 40)
    
    first_doc = collection.documents[0]
    html_output = DocumentProcessor.markdown_to_html(first_doc.content)
    print(f"✅ Converted document: {first_doc.metadata.get('source')}")
    print("\nFirst 500 chars of HTML output:")
    print("-" * 40)
    print(html_output[:500] + "...\n")
    
    # Step 4: Split into sections
    print("STEP 4: SPLITTING INTO SECTIONS")
    print("-" * 40)
    
    sections = DocumentProcessor.extract_sections(first_doc, min_words=10)
    print(f"✅ Split into {len(sections)} sections\n")
    
    for i, section in enumerate(sections[:3], 1):
        print(f"   Section {i}: {section.metadata.get('section_title')}")
        print(f"      Words: {len(section.content.split())}")
        print(f"      Preview: {section.content[:100]}...\n")
    
    # Step 5: Create document graph
    print("STEP 5: DOCUMENT RELATIONSHIP GRAPH")
    print("-" * 40)
    
    graph = collection.create_document_graph()
    print(f"✅ Graph created with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges\n")
    
    print("   Document Nodes:")
    for node in graph['nodes']:
        print(f"      📄 {node['id']} ({node['heading_count']} headings)")
    
    print("\n   Document Links (Edges):")
    for edge in graph['edges']:
        print(f"      🔗 {edge['from']} → {edge['to']} ('{edge['text']}')")
    
    # Step 6: Structure summary
    print("\nSTEP 6: COMPLETE STRUCTURE SUMMARY")
    print("-" * 40)
    
    all_structures = []
    for doc in collection.documents:
        structure = doc.get_structure_summary()
        all_structures.append(structure)
        
        print(f"\n📄 {doc.metadata.get('source')}:")
        print(f"   ID: {structure['id']}")
        print(f"   Content Length: {structure['content_length']} chars")
        print(f"   Word Count: {structure['word_count']}")
        print(f"   Headings: {structure['heading_count']}")
        print(f"   Links: {structure['link_count']}")
    
    # Step 7: Save structure as JSON for analysis
    print("\nSTEP 7: EXPORTING STRUCTURE DATA")
    print("-" * 40)
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'document_count': len(collection.documents),
        'documents': all_structures,
        'graph': graph,
        'total_headings': len(collection.get_all_headings()),
        'total_links': len(collection.get_all_links())
    }
    
    # Save to file (uncomment to actually save)
    # with open('document_structure.json', 'w') as f:
    #     json.dump(export_data, f, indent=2)
    
    print("✅ Structure data ready (would be saved to JSON)")
    print(f"   Total Headings: {export_data['total_headings']}")
    print(f"   Total Links: {export_data['total_links']}")
    
    # Step 8: Explain how this applies to LangChain
    print("\n" + "=" * 60)
    print("🔗 HOW THIS APPLIES TO LANGCHAIN")
    print("=" * 60)
    
    print("""
    1. DOCUMENT LOADING
       → Use DocumentLoaders to load markdown/HTML files
       → Structure is preserved in Document objects
       → Metadata tracks source, type, and loading time
    
    2. TEXT SPLITTING
       → Split by headings (markdown #, ##, ###)
       → Each section becomes a separate chunk
       → Preserve structural context for better retrieval
    
    3. EMBEDDING
       → Include heading context in embedding text
       → Preserve document hierarchy in vectors
       → Better semantic understanding of structure
    
    4. RETRIEVAL
       → Search with structural awareness
       → Return relevant sections with context
       → Maintain document relationships
    
    5. LINK ANALYSIS
       → Track internal and external links
       → Build document relationship graphs
       → Understand information flow in your system
    """)
    
    print("=" * 60)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\n🎯 Key Takeaway: Document structure (headings, links, sections)")
    print("   is preserved and used throughout the processing pipeline.")
    print("   This is exactly how LangChain processes documents.\n")

# ============================================================
# PART 5: RUN THE DEMONSTRATION
# ============================================================

if __name__ == "__main__":
    demonstrate_document_processing()