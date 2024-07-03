from langchain_core.tools import tool
from langchain_community.vectorstores import Qdrant
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import JinaRerank
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_exa import ExaSearchRetriever, TextContentsOptions
from langchain_community.retrievers import WikipediaRetriever

import dotenv
import pickle 
import os

dotenv.load_dotenv()
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
os.environ['EXA_API_KEY'] = os.getenv('EXA_API_KEY')
NVIDIA_NIM_API_KEY = os.getenv('NVIDIA_NIM_API_KEY')
JINA_API_KEY = os.getenv('JINA_API_KEY')


embeddings = NVIDIAEmbeddings(model='nvidia/nv-embed-v1', nvidia_api_key=NVIDIA_NIM_API_KEY)


wikipedia_retriever = WikipediaRetriever(load_all_available_meta=True, top_k_results=1, features='lxml')
tavily_search = TavilySearchResults(max_results=5)

with open('reference_docs.pkl', 'rb') as f:
    loaded_array = pickle.load(f)
reference_docs = loaded_array

vectorstore = Qdrant.from_documents(
    reference_docs,
    embedding=embeddings,
    location=':memory:',
    collection_name="references",
)

retriever = vectorstore.as_retriever(k=15)

compressor = JinaRerank(jina_api_key=JINA_API_KEY, model='jina-reranker-v2-base-multilingual', top_n=10)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

exa_retriever = ExaSearchRetriever(k=3, 
                                  include_domain=['twitter.com', 'youtube.com', 'medium.com'],
                                  use_autoprompt=True, 
                                  text_contents_options=TextContentsOptions(max_characters=1000)
                                )


def format_doc(doc, max_length=1000):
  related = '-'.join(doc.metadata['related_titles'])
  return f"""### {doc.metadata['title']}\n\nSummary: {doc.page_content}\n\nRelated\n{related}"""[:max_length]

def format_docs(docs):
  return "\n\n".join(format_doc(doc) for doc in docs)

@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]


async def retrieve(inputs: dict):
    docs = await compression_retriever.ainvoke(inputs["topic"] + ": " + inputs["section"])
    search = await exa_retriever.ainvoke(inputs["section"])
    formatted = "\n".join(
        [
            f'<Document href="{doc.metadata["source"]}"/>\n{doc.page_content}\n</Document>'
            for doc in docs 
        ]
    )

    formatted_src = "\n".join(
        [
            f'<Document href="{doc.metadata["url"]}"/>\n{doc.page_content}\n</Document>'
            for doc in search 
        ]
    )

    return {"docs": formatted, "src": formatted_src, **inputs}

