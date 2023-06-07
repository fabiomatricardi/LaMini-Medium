import ssl
########### SSL FOR PROXY ##############
ssl._create_default_https_context = ssl._create_unverified_context


#### IMPORTS FOR AI PIPELINES ###############
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

from transformers import AutoModel, T5Tokenizer, T5Model
from transformers import T5ForConditionalGeneration
from langchain.llms import HuggingFacePipeline
import torch
#from functools import reduce  #for highlighter
#from itertools import chain   #for highlighter
import datetime
import os
import requests
from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace models
from langchain import HuggingFaceHub
# PUT HERE YOUR HUGGING FACE API TOKEN shuold start with hf_XXXXXXX...
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
#############################################################################
#               SIMPLE TRANSLATION GENERATION INFERENCE
#           checkpoint = "./model_it/  Helsinki-NLP/opus-mt-en-it
# ###########################################################################

from rich import console
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from functools import reduce
from itertools import chain
import datetime

console = Console()

#LOCAL MODEL EN-IT
#---------------------------------
#  Helsinki-NLP/opus-mt-en-it
Model_IT = './model_it/'   #torch
#---------------------------------

pippo = """
Introduction
We rely on google translate services to help us with translating text from one language to other and I always wanted to develop an app like that and to know how translation works in the backend.

Let’s list down the components which will be there in our translate app.

These are those components -

A Multi-language translation model.
An API service which takes all the necessary parameters sends those parameters to the model and returns the translated text back as response.
A front-end app which provides a GUI to the user to interact with.
An ideal flow will look like user typing a text in the input text, selecting the desired target language and clicking the translate button. Once the button is clicked, we get the request data and send to the API service which eventually passes that to the model and get the results back as a response. The response is then shown into the UI.

The Big Challenge
The ML model is going to be the brain behind our translation app. To train a state-of-the-art model from scratch we would need the following things -

Huge amounts of training data containing examples of text in one language and its translation in the other language.
Create a neural network model which consists of more than a million parameters.
A high end multi-GPU based environment to train that model.
Time.
But my goal here is to develop a MVP or a small POC which could help me understand and demonstrate the process of making a translation app and be able to complete this over a weekend.

HuggingFace to the rescue
The solution is that we can use a pre-trained model which is trained for translation tasks and can support multiple languages.

HuggingFace consists of an variety of transformers/pre-trained models. One of the translation models is MBart which was presented by Facebook AI research team in 2020 — Multilingual Denoising Pre-training for Neural Machine Translation.

Great!! Now that we have a pre-trained model in place. Time to put the pieces of the puzzle in the right places.
"""
with console.status("Preparing model and pipeline...", spinner="monkey"):   
    from langchain.text_splitter import CharacterTextSplitter
    # TEXT SPLITTER FUNCTION FOR CHUNKING
    text_splitter = CharacterTextSplitter(        
        separator = "\n\n",
        chunk_size = 300,
        chunk_overlap  = 0,
        length_function = len,
    )
    # CHUNK THE DOCUMENT
    console.print('[bold blue] Chunking the text...')
    texts = text_splitter.create_documents([pippo])
    console.print('[bold red] Inizialize AI toknizer...')
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    # INITIALIZE TRANSLATION FROM ENGLISH TO ITALIAN

    tokenizer_tt0it = AutoTokenizer.from_pretrained(Model_IT)  #google/byt5-small   #facebook/m2m100_418M
    console.print('[bold green] Inizialize AI model...')
    model_tt0it = AutoModelForSeq2SeqLM.from_pretrained(Model_IT)  #Helsinki-NLP/opus-mt-en-it  or #Helsinki-NLP/opus-mt-it-en
    TToIT = pipeline("translation", model=model_tt0it, tokenizer=tokenizer_tt0it)
# Example    TToIT("How old are you?")[0]['translation_text']

# ITERATE OVER CHUNKS AND JOIN THE TRANSLATIONS
finaltext = ''
start = datetime.datetime.now() #not used now but useful
console.print('[bold yellow] Translation in progress...')
for item in texts:
  line = TToIT(item.page_content)[0]['translation_text']
  finaltext = finaltext+line+'\n'
stop = datetime.datetime.now() #not used now but useful
elapsed = stop - start
console.print(f'[bold underline green1] Translation generated in [reverse dodger_blue2]{elapsed}[/reverse dodger_blue2]...')
console.print(Panel(finaltext, title="AI Translatio", title_align="center"))


