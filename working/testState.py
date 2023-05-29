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

with open('video_transcript.txt') as f:
    testo = f.read()
f.close()

global video_summary
global processed
processed = False
#with st.columns(3)[1]:
#     st.header("hello world")
#     st.image("http://placekitten.com/200/200")
#st.title('🏞️ Image display methods')
#
#st.write("a logo and text next to eachother")
#

### HEADER section
col1, col2, col3 = st.columns([1,20, 1])
col2.image('youtubelogo.jpg', width=180)
col2.title('AI Summarizer')

#image_path = 'logo.png'
#image = Image.open(image_path)
#st.image('https://streamlit.io/images/brand/streamlit-mark-light.png')
#st.image(image_path, width = 700)


title = st.text_input('1. Input your Youtube Video url', 'Something like https://youtu.be/SCYMLHB7cfY....', key='inputurl')   #https://youtu.be/SCYMLHB7cfY
videotitle = st.empty()
st.write(st.session_state.inputurl)

txt = st.empty()
video_dur = st.empty()
video_redux = st.empty()
st.divider()




txt.text_area('Summarized text', testo, height = 450, key = 'result')
def putto():
    st.session_state.result = testo
st.write(st.session_state.result)
video_redux.markdown(f"Percentage of reduction: 15   {len(testo[:350].split(' '))}/{len(testo.split(' '))} words")
if st.button('2. Start Summarization', on_click=putto):
    processed = True #stuts for the download button
    print(processed)
    st.write(st.session_state.result)


if st.button('3. Download Summarization'):
    with open('putto.txt', 'w') as f:
        f.write(st.session_state.result)
    f.close()
    st.markdown(f"## Download your YouTube Video Summarization")
    st.success('AI Summarization saved in video_summarization.txt', icon="✅")



