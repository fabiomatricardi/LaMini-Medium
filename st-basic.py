import streamlit as st
############# Displaying images on the front end #################
st.set_page_config(page_title="Mockup for single page webapp",
                   page_icon='💻',
                   layout="centered",  #or wide
                   initial_sidebar_state="expanded",
                   menu_items={
                        'Get Help': 'https://docs.streamlit.io/library/api-reference',
                        'Report a bug': "https://www.extremelycoolapp.com/bug",
                        'About': "# This is a header. This is an *extremely* cool app!"}
                        )
# Load image placeholder from the web
st.image('https://placehold.co/1172x368', width=750)
st.divider()
# load image from local disk
st.image('Headline-text.jpg', width=750)
st.divider()
st.image('750x250.svg', width=750)