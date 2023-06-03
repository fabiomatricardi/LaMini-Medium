# MODEL FOR KOREAN TRANSLATIONS
https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-ko/tree/main
repo_id = 'Helsinki-NLP/opus-mt-tc-big-en-ko'

### Use in Transformers
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-big-en-ko")

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-tc-big-en-ko")
```


### MODEL FOR KOREAN TRANSLATIONS AND SUMMARIZATION
BAD
repo_id = 'gogamza/kobart-base-v2'
---
files and model card:
https://huggingface.co/gogamza/kobart-base-v2/tree/main

GitHub repo with examples: https://github.com/haven-jeon/KoBART

KoBart translations Inference
https://github.com/seujung/KoBART-translation/blob/main/infer.py
KoBart SUMMARIZATION
https://github.com/seujung/KoBART-summarization
