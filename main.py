import os
import requests
# PUT HERE YOUR HUGGING FACE API TOKEN shuold start with hf_XXXXXXX...
#os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_XXXXXXXX"

#from langchain.document_loaders import TextLoader  #for textfiles
from langchain.loaders import TextLoader  #for textfiles
from langchain.text_splitter import CharacterTextSplitter #text splitter
from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace models
from langchain.vectorstores import FAISS  #facebook vectorizationfrom langchain.chains.question_answering import load_qa_chain
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub