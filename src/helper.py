
from langchain.embeddings import HuggingFaceEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain.llms import CTransformers
from accelerate import Accelerator
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_embedding_model():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}
    embedding_model = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embedding_model



def get_indexed_data(embedding_model,dbname):
    db = Pinecone.from_existing_index(dbname, embedding_model)
    return db

def get_llm():
    config = {'max_new_tokens': 512,'context_length': 8000}

    llm = CTransformers( 
                        model='TheBloke/Llama-2-7B-Chat-GGUF',
                        model_file="llama-2-7b-chat.Q4_K_S.gguf",
                        config=config,
                        model_type='llama',
                        device = 'cuda',
                        temprature=0.8 )

    
    accelerator = Accelerator()
    llm, config = accelerator.prepare(llm, config)
    return llm 

def get_chain_and_memory(llm,template):
    
    prompt = PromptTemplate(input_variables=["chat_history", "query", "context"], template=template)
    memory = ConversationBufferMemory(memory_key="chat_history", input_key="query")

    chain = load_qa_chain(llm, chain_type="stuff", memory=memory, prompt=prompt)

    return chain,memory

def generate_chats(chat_history):
    chats=chat_history.split('Human:')[1:]
    out_chats=[]
    for chat in chats:
        a=chat.split('AI:')
        temp=[]
        temp.append(a[0])
        a[1]=a[1].replace('\n','<br>')
        temp.append(a[1])
        out_chats.append(temp)

    return out_chats 

def get_response(text):
    from openai import OpenAI
    import os
    
    client = OpenAI(api_key="")
    

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content":text},
    ]
    )
    return response.choices[0].message.content

