#################### VIDEO AND SCRIPT SECTION #############################
# Extract Video Informations for future use in PDF or word processor
# Prepare the text for Summarization (no fuss, plain text)
###########################################################################
import ssl
from pytube import YouTube as YT
import re
import textwrap

# SSL for proxied internet access
ssl._create_default_https_context = ssl._create_unverified_context

# paste here the url of the youtubevideo you want
url = "https://youtu.be/SCYMLHB7cfY" # or https://youtu.be/5g1z4Sr-UHM 
# we instantiate a YouTube object already with our 
myvideo = YT(url, use_oauth=True, allow_oauth_cache=True)
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
#print(caption)

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
print(wrapped_text)
with open('video_transcript.txt', 'w') as f:
    f.write(to_sum_text)
f.close()
print('File video_transcript.txt saved')


"""
#print(final_text)
#PREPARE A LONG STRING FOR THE SUMMARIZATION, no Video Description Here
intro_summarization = 'Video Title: '+myvideo.title+' - (video url: )'+url+' ---  '+'\n'
#PREPARE A LONG TEXT with details and Video Description Here: to be used
#as a note or Blog
intro_blog = 'Video Title: '+myvideo.title+'\n'+'Video url: '+url+'\n'+'-------------'+'\n'
summarization_text = intro_summarization + final_text
import textwrap
blog_text = m_intro + textwrap.fill(final_text, 70)

def correct_filename_cr(title):
  string = title
  finalfilename = ''.join(e for e in string if e.isalnum())+'_cr.txt'
  return finalfilename
def correct_filename_nocr(title):
  string = title
  finalfilename = ''.join(e for e in string if e.isalnum())+'_nocr.txt'
  return finalfilename

print("Saving to TXT file...")
filename_file = correct_filename_cr(myvideo.title) #with carriage return
filename_summary = correct_filename_nocr(myvideo.title) #with no carriege return

#prepare the text for the Blog or Notes
#with carriage return
import textwrap
wrapped_text = textwrap.fill(final_text, 100)

# write the cleaned up text into a file called final_text.txt
with open(filename_file, 'w') as f:
    f.write(blog_text)
f.close()
with open(filename_summary, 'w') as f:
    f.write(summarization_text)
f.close()
"""











"""
import ssl
import requests

########### SSL FOR PROXY ##############
ssl._create_default_https_context = ssl._create_unverified_context

response = requests.get('https://github.com/fabiomatricardi/pytubeFix/raw/main/1213-python10/captions.py')

with open('captions.py', 'w') as f:
    f.write(response)
f.close()

response = requests.get('https://github.com/fabiomatricardi/pytubeFix/raw/main/1213-python10/cipher.py')

with open('cipher.py', 'w') as f:
    f.write(response)
f.close()


 """