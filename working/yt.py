from pytube import YouTube as YT
import ssl
import datetime

########### SSL FOR PROXY ##############
ssl._create_default_https_context = ssl._create_unverified_context

myvideo = YT('https://youtu.be/riXpu1tHzl0', use_oauth=True, allow_oauth_cache=True)
# required only for the first time to know what languages are aavailable
print(myvideo.title)
print(myvideo.captions) #print the options of languages available
#Commented for automatically choice to auto-generated
#code = input("input the code you want: ")  #original
print("Scraping subtitles...")
#Commented to test the auto-generated ones
#sub = myvideo.captions[code]  #original 
print(myvideo.captions)
sub = myvideo.captions['a.en']
print(sub)
caption = sub.generate_srt_captions()
import datetime
m1 = f"TITLE: {myvideo.title}"+'\n'
m2 = f"thumbnail url: {myvideo.thumbnail_url}"+'\n'
m4 = f"video Duration: {str(datetime.timedelta(seconds=myvideo.length))}"+'\n'
m5 = "----------------------------------------"+'\n'
#m6 = textwrap.fill(myvideo.description, 80)+'\n'  #solution not good
m6 = myvideo.description+'\n'
m7 = "----------------------------------------"+'\n'
     