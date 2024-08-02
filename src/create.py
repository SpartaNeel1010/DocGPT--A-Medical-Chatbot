from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.vectorstores import Pinecone
import os

def split_text(content):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        length_function=len)
    doc_chunks=text_splitter.split_text(content)
    return doc_chunks

def get_embedding():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding_model = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs,encode_kwargs=encode_kwargs)
    return embedding_model

def add_data_to_vectordb(content,dbname):
    embedding_model=get_embedding()
    doc_chunks=split_text(content)
    os.environ['PINECONE_API_KEY'] = ""
    os.environ['PINECONE_API_ENV'] = "gcp-starter"
    os.environ["HUGGINGFACEHUB_API_TOKEN"]=""
    print(doc_chunks)
    print(len(doc_chunks)) 
    Pinecone.from_texts(doc_chunks,embedding_model,index_name=dbname)
    print("done")

def create_index(dbname,user_id):
    from pinecone import Pinecone, ServerlessSpec

    api_key = ""
    pc = Pinecone(api_key=api_key)

    index_name = dbname
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    add_database1(dbname,user_id)
    
    print("Vector db created succesfully")
def add_database1(dbname,user_id):
    try: 
        from pymongo import MongoClient
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.user_vectordbs
        databases=collection.find({'user_id':user_id})[0]['databases']
        databases.append(dbname)
        collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"databases": databases}}
                )

    except Exception as e:
        print(e)








    
