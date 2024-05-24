import requests
import warnings
import os.path as osp
from pathlib import Path

import pandas as pd
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.schema.document import Document
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(model="llama2", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
map_prompt_template = """
                      Write a very summary of this chunk of text that includes the main points and any important details.
                      {text}
                      """

map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

combine_prompt_template = """
                      Write a very short and concise summary of the following text delimited by triple backquotes.
                      Return your response in bullet points which covers the key points of the text.
                      
{text}
                      BULLET POINT SUMMARY:
                      """

combine_prompt = PromptTemplate(
    template=combine_prompt_template, input_variables=["text"]
)
map_reduce_chain = load_summarize_chain(
    llm,
    chain_type="map_reduce",
    map_prompt=map_prompt,
    combine_prompt=combine_prompt,
    return_intermediate_steps=True,
)


def summarize_texts(results: dict):
    docs = [
        Document(page_content=v)
        for _, v in results.items()
    ]
    map_reduce_outputs = map_reduce_chain({"input_documents": docs})
    return {
        k: map_reduce_outputs["intermediate_steps"][i] 
        for i, k in enumerate(results.keys())
    }