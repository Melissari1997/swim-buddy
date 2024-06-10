import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


def create_vector_db():
    """
    Function to create a vector database from PDF documents.

    This function loads PDF documents from a specified directory, splits the text content
    of these documents into manageable chunks, generates embeddings for these chunks,
    and stores the embeddings in a FAISS vector database.
    """
    # Load PDF documents from the directory specified by the DATA_PATH environment variable
    loader = DirectoryLoader(os.getenv("DATA_PATH"), glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()

    # Split the loaded documents into smaller chunks for embedding
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Initialize HuggingFace embeddings with a specified model_name
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    # Create a FAISS vector database from the document chunks and their embeddings
    db = FAISS.from_documents(texts, embeddings)

    # Save the FAISS database locally to the path specified by the DB_FAISS_PATH environment variable
    db.save_local(os.getenv("DB_FAISS_PATH"))


if __name__ == "__main__":
    # Entry point of the script
    create_vector_db()
