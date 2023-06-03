# Korean model
This is used ONLY for translations from English to Korean (Hangul)

source: https://huggingface.co/hcho22/opus-mt-ko-en-finetuned-en-to-kr
reo_id = "hcho22/opus-mt-ko-en-finetuned-en-to-kr"

NOTE
tensorflow is required
the modiule has extension h5
```
pip install tensorflow
Successfully installed absl-py-1.4.0 astunparse-1.6.3 flatbuffers-23.5.26 gast-0.4.0 google-auth-2.19.1 google-auth-oauthlib-1.0.0 google-pasta-0.2.0 grpcio-1.54.2 h5py-3.8.0 jax-0.4.11 keras-2.12.0 libclang-16.0.0 ml-dtypes-0.1.0 oauthlib-3.2.2 opt-einsum-3.3.0 pyasn1-0.5.0 pyasn1-modules-0.3.0 requests-oauthlib-1.3.1 rsa-4.9 tensorboard-2.12.3 tensorboard-data-server-0.7.0 tensorflow-2.12.0 tensorflow-estimator-2.12.0 tensorflow-intel-2.12.0 tensorflow-io-gcs-filesystem-0.31.0 termcolor-2.3.0 urllib3-1.26.16 werkzeug-2.3.4 wheel-0.40.0
```
INCLUDE in the IMPORT for tokenizer `from_tf=True`
```
model_ttKR = AutoModelForSeq2SeqLM.from_pretrained(Model_KR, from_tf=True)
```

Some tests examples