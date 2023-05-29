########### GUI IMPORTS ################
import streamlit as st
import pandas as pd
from io import StringIO
from PIL import Image
import ssl


############# Displaying images on the front end #################
st.set_page_config(page_title="Summarize and Talk ot your Documents",
                   page_icon='📖',
                   layout="centered",  #or wide
                   initial_sidebar_state="expanded",
                   menu_items={
                        'Get Help': 'https://docs.streamlit.io/library/api-reference',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!"
                                },
                   )
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

#############################################################################
#               SIMPLE TEXT2TEXT GENERATION INFERENCE
#           checkpoint = "./models/LaMini-Flan-T5-783M.bin" 
# ###########################################################################
checkpoint = "./model/"  #it is actually LaMini-Flan-T5-248M
LaMini = './model/'


######################################################################
#     SUMMARIZATION FROM TEXT STRING WITH HUGGINGFACE PIPELINE       #
######################################################################
def AI_SummaryPL(checkpoint, text, chunks, overlap):

    """
    checkpoint is in the format of relative path
    example:  checkpoint = "/content/model/"  #it is actually LaMini-Flan-T5-248M   #tested fine
    text it is either a long string or a input long string or a loaded document into string
    chunks: integer, lenght of the chunks splitting
    ovelap: integer, overlap for cor attention and focus retreival
    RETURNS full_summary (str), delta(str) and reduction(str)

    post_summary14 = AI_SummaryPL(LaMini,doc2,3700,500)
    USAGE EXAMPLE:
    post_summary, post_time, post_percentage = AI_SummaryPL(LaMini,originalText,3700,500)
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = chunks,
        chunk_overlap  = overlap,
        length_function = len,
    )
    texts = text_splitter.split_text(text)
    #checkpoint = "/content/model/"  #it is actually LaMini-Flan-T5-248M   #tested fine
    checkpoint = checkpoint
    tokenizer = T5Tokenizer.from_pretrained(checkpoint)
    base_model = T5ForConditionalGeneration.from_pretrained(checkpoint,
                                                        device_map='auto',
                                                        torch_dtype=torch.float32)
    ### INITIALIZING PIPELINE
    pipe_sum = pipeline('summarization', 
                        model = base_model,
                        tokenizer = tokenizer,
                        max_length = 350, 
                        min_length = 25
                        )
    ## START TIMER
    start = datetime.datetime.now() #not used now but useful
    ## START CHUNKING
    full_summary = ''
    for cnk in range(len(texts)):
      result = pipe_sum(texts[cnk])
      full_summary = full_summary + ' '+ result[0]['summary_text']
    stop = datetime.datetime.now() #not used now but useful  
    ## TIMER STOPPED AND RETURN DURATION
    delta = stop-start  
    ### Calculating Summarization PERCENTAGE
    reduction = '{:.1%}'.format(len(full_summary)/len(text))
    print(f"Completed in {delta}")
    print(f"Reduction percentage: ", reduction)
    
    return full_summary, delta, reduction

testo = """Title: BERT: A Beginner-Friendly Explanation | by Digitate | May, 2023 | Medium
-------------------------------------------------------------------------------
written By Pushpam Punjabi
author Pushpam Punjabi

Up until now, we’ve seen how a computer understands the meaning of different words using word embeddings. In the last blog, we also looked at how we can take average of the embeddings of words appearing in a sentence to represent that sentence as an embedding. This is one of the ways of interpreting a sentence. But that’s not how humans understand the language. We don’t just take individual meaning of words and form the understanding of a sentence or a paragraph. A much more complex process is involved to understand language by humans. But how does a machine understand language? It’s through language models!

Language models are an essential component of Natural Language Processing (NLP), designed to understand and generate human language. They use various statistical and machine learning techniques to analyze and learn from large amounts of text data, enabling them to identify patterns and relationships between words, phrases, and sentences. Word embeddings form the base in understanding these sentences! Language models have revolutionized the field of NLP and have played a crucial role in enabling machines to interact with humans in a more natural and intuitive way. Language models have also surpassed humans in some of the tasks in NLP!

In this blog, we will understand Bi-directional Encoder Representations from Transformers (BERT) which is one of the biggest milestones in the world on language models!

Understanding BERT

BERT was developed by Google in 2018. It is a “Language Understanding” model, that is trained on a massive amounts of text data to understand the context and meaning of words and phrases in a sentence. BERT uses “transformer” deep learning architecture that enables it to process information bidirectionally, meaning it can understand the context of a word based on both, the words that come before and after it. This allows BERT to better understand the nuances of language, including idioms, sarcasm, and complex sentence structures.

You must be wondering how do you train such models to understand human language? There are 2 training steps involved to use BERT:

Pre-training phase
Fine-tuning phase
1. Pre-training phase

In pre-training phase, the model is trained on huge textual data. This is the stage where the model learns and understand the language. Pre-training is expensive. To pre-train a BERT model, Google used multiple TPUs — special computing processors for deep learning models. It took them 4 days to pre-train BERT on such a large infrastructure. But this is only a one-time procedure. Once the model understands the language, we can reuse the model for variety of tasks in NLP. There are 3 steps to pre-train BERT:"""



#with st.columns(3)[1]:
#     st.header("hello world")
#     st.image("http://placekitten.com/200/200")
#st.title('🏞️ Image display methods')
#
#st.write("a logo and text next to eachother")
#

### HEADER section
st.image('youtubelogo.jpg', width=180)
st.title('AI Summarizer')

image_path = 'logo.png'
#image = Image.open(image_path)
#st.image('https://streamlit.io/images/brand/streamlit-mark-light.png')
st.image(image_path, width = 700)


title = st.text_input('1. Input your Youtube Video url', 'https://youtu.be/....')   #https://youtu.be/SCYMLHB7cfY
st.write('The current Youtube link is', title)

txt = st.empty()
video_dur = st.empty()
video_redux = st.empty()

video_summary = ''
def start_sum(text):
    if '...' in text:
        st.warning('Wrong youtube video link \n Type a valid url like https://youtu.be/SCYMLHB7cfY', icon="⚠️")
    else:
        st.success('AI process started', icon="✅")
        print("Starting AI pipelines")
        video_summary, duration, reduction = AI_SummaryPL(LaMini,testo,3700,500)
        txt.text_area('Summarized text', video_summary, height = 300, key = 'result')
        video_dur.text(f'Processing time :clock3: :, {duration}')
        video_redux.text(f'Percentage of reduction: {reduction}')

if st.button('2. Start Summarization'):
    start_sum(title)
else:
    st.write('Insert the video url in the input box above...')

st.divider()


if st.button('3. Download Summarization'):
    st.wrte("Download in proress...")
else:
    st.write('Insert the video url in the input box above...')

st.divider()
uploaded_file = st.file_uploader("Choose a file", key='txtup', type={"txt"})

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    #dataframe = pd.read_csv(uploaded_file)
    #st.write(dataframe)

more_files = st.file_uploader("Choose a CSV file", type={"csv"}, key='csvup')
if more_files is not None:
    #stringio = StringIO(more_files.getvalue().decode("utf-8"))
    dataframe = pd.read_csv(more_files)
    st.write(dataframe)