from langchain.document_loaders import UnstructuredURLLoader
# required tabulate  pip install tabulate
# requires also libmagic   pip install libmagic
import ssl

#if error see comments at the end

ssl._create_default_https_context = ssl._create_unverified_context

urls = [
    "https://keras.io/examples/nlp/t5_hf_summarization/",
    "https://blog.futuresmart.ai/summarizing-documents-made-easy-with-langchain-summarizer"
]

loader = UnstructuredURLLoader(urls=urls)
data = loader.load()
print("unstructerLoader...")
print("*"*50)
print(data)

# WebBaseLoader   requires  `pip install bs4`
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader(urls[0])
data2 = loader.load()
print("WbeBaseloader...")
print("*"*50)
print(data2)

#Loading multiple webpages
#You can also load multiple webpages at once by passing in a list of urls to the loader. 
#This will return a list of documents in the same order as the urls passed in.

loader = WebBaseLoader(["https://www.espn.com/", "https://google.com"])
docs = loader.load()
docs

"""
SOURCE https://stackoverflow.com/questions/51925384/unable-to-get-local-issuer-certificate-when-using-requests-in-python
---
Error fetching or processing https://blog.futuresmart.ai/summarizing-documents-made-easy-with-langchain-summarizer, exeption: HTTPSConnectionPool(host='blog.futuresmart.ai', port=443): Max retries exceeded with url: /summarizing-documents-made-easy-with-langchain-summarizer (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
1. to chech if you have certificates
python -c "import ssl; print(ssl.get_default_verify_paths())"

if empty run python
>>> import certifi
>>> certifi.where()
'C:\\Users\\fmatricard\\Videos\\LaMiniLocal\\venv\\lib\\site-packages\\certifi\\cacert.pem'

save the certificate from every url click on the locker, details export BASE64 encoded .cer files

open venv\\lib\\site-packages\\certifi\\cacert.pem' and append the entire certificated between the 2 tags...
(---Begin Certificate--- *** ---End Certificate---)


ALTERNATIVE

For those who this problem persists: - Python 3.6 (some other versions too?) on MacOS comes with its own private copy of OpenSSL. That means the trust certificates in the system are no longer used as defaults by the Python ssl module. To fix that, you need to install a certifi package in your system.

You may try to do it in two ways:

1) Via PIP:

pip install --upgrade certifi
2) If it doesn't work, try to run a Cerificates.command that comes bundled with Python 3.6 for Mac:

open /Applications/Python\ 3.6/Install\ Certificates.command
One way or another, you should now have certificates installed, and Python should be able to connect via HTTPS without any issues.

"""