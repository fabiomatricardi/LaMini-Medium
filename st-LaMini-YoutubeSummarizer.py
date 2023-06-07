########### GUI IMPORTS ################
import streamlit as st
import pandas as pd
from io import StringIO
from PIL import Image
import ssl
from pytube import YouTube as YT
import re
import textwrap


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


global video_summary

#with st.columns(3)[1]:
#     st.header("hello world")
#     st.image("http://placekitten.com/200/200")
#st.title('🏞️ Image display methods')
#
#st.write("a logo and text next to eachother")
#

### HEADER section
st.image('Headline.jpg', width=750)
#title('AI Summarizer')

#image_path = 'logo.png'
#image = Image.open(image_path)
#st.image('https://streamlit.io/images/brand/streamlit-mark-light.png')
#st.image(image_path, width = 700)


title = st.text_input('1. Input your Youtube Video url', 'Something like https://youtu.be/SCYMLHB7cfY....')   #https://youtu.be/SCYMLHB7cfY
videotitle = st.empty()

btt = st.empty()
txt = st.empty()
video_dur = st.empty()
video_redux = st.empty()
st.divider()

video_summary = ''
def start_sum(text):
    if '...' in text:
        st.warning('Wrong youtube video link! Type a valid url like https://youtu.be/SCYMLHB7cfY', icon="⚠️")
    else:
        myvideo = YT(title, use_oauth=True, allow_oauth_cache=True)
        # required only for the first time to know what languages are aavailable
        print(myvideo.title)
        print(myvideo.captions) #print the options of languages available
        #Commented for automatically choice to auto-generated
        #code = input("input the code you want: ")  #original
        print("Scraping subtitles...")
        #Commented to test the auto-generated ones
        #sub = myvideo.captions[code]  #original 
        sub = myvideo.captions['a.en']
        caption = sub.generate_srt_captions()
        #print(caption)#print(caption)

        # Club Video Title, details and Description, only for printed version
        # not for the Sumarization one
        # possible in future to prepare for Markdown to PDF export
        import datetime
        m1 = f"TITLE: {myvideo.title}"+'\n'
        m2 = f"thumbnail url: {myvideo.thumbnail_url}"+'\n'
        m4 = f"video Duration: {str(datetime.timedelta(seconds=myvideo.length))}"+'\n'
        m5 = "----------------------------------------"+'\n'
        #m6 = textwrap.fill(myvideo.description, 80)+'\n'  #solution not good
        m6 = myvideo.description+'\n'
        m7 = "----------------------------------------"+'\n'
        m_intro = m1+m2+m4+m5+m6+m7

        # Function to clean up the srt text
        def clean_sub(sub_list):
            lines = sub_list
            text = ''
            for line in lines:
                if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                    text += ' ' + line.rstrip('\n')
                text = text.lstrip()
            #print(text)
            return text

        print("Transform subtitles to TEXT...")
        srt_list = str(caption).split('\n')  #generate a list with all lines
        final_text = clean_sub(srt_list)

        to_sum_text = m1+m4+m5+final_text
        wrapped_text = textwrap.fill(to_sum_text, 100)
        with open('video_transcript.txt', 'w') as f:
            f.write(to_sum_text)
        f.close()
        print('File video_transcript.txt saved')

        videotitle.markdown(f"Video title: **{myvideo.title}**")
        print("Starting AI pipelines")
        video_summary, duration, reduction = AI_SummaryPL(LaMini,to_sum_text,3700,500)
        txt.text_area('Summarized text', video_summary, height = 350, key = 'result')
        video_dur.markdown(f'Processing time :clock3: :, {duration}')
        video_redux.markdown(f"Percentage of reduction: {reduction}   **{len(video_summary.split(' '))}**/{len(to_sum_text.split(' '))} words")


if btt.button('2. Start Summarization', key='start'):
    with st.spinner('Initializing pipelines...'):
        st.success(' AI process started', icon="🤖")
        start_sum(title)
else:
    st.write('Insert the video url in the input box above...')

if st.button('3. Download Summarization'):
    st.markdown(f"## Download your YouTube Video Summarization")
    def savefile(generated_summary, filename):
        st.write("Download in progress...")
        with open(filename, 'w') as t:
            t.write(generated_summary)
        t.close()
        st.success(f'AI Summarization saved in {filename}', icon="✅")
    savefile(st.session_state.result, 'video_summarization.txt')
    txt.text_area('Summarized text', st.session_state.result, height = 350)



