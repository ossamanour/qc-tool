import os
from openai import AzureOpenAI
import pandas as pd
import numpy as np
from collections import defaultdict
from collections import deque
import json
from urllib.request import Request, urlopen
import urllib.parse
import time
import requests, codecs

# set up parameters related to chatbot api
ML_SERVER_URL = "http://20.172.64.197:5000/"

config = {
    'azure_openai_completion_deployment': "gpt-4o-mini",
    'azure_openai_endpoint': "https://chat-gen-oai.openai.azure.com/",
    'azure_openai_completion_api_version': "2024-02-01",
    
}

_client = {'completion': AzureOpenAI(
                azure_endpoint = config['azure_openai_endpoint'],
                api_key = config['azure_openai_api_key'],
                api_version = config['azure_openai_completion_api_version']
            )
}

_system_prompts = {}
_system_prompts['qa'] = "You are an AI assistant specializing in regulatory and policy-related inquiries. Your responses should be thorough, precise, and based strictly on the provided information. If the requested information is not explicitly mentioned, state that it is not addressed. Avoid making legal interpretations beyond the text but summarize relevant provisions in detail. Provide references to specific sections when applicable. And Use Tools when necessary"



# get inforamtion from chatbot
def get_chatbot_response(city, zone, prompt):
    chat_config = {
        'city': city,
        'zone': zone,
        'zone_codes': dict(),
        'zone_groups': dict(),
        'system_prompt': _system_prompts['qa'],
        'tool_option': 'ChatPlus',
        'zone_category': '',
        'chat_type': 'Query All',
        'prompt': prompt,
        'session_site_address': '',
        'prompt_type' : 'qa'
    }
    response_text = ''
    response = requests.post(
        ML_SERVER_URL+'predict_response', 
        json={"prompt": prompt, "chat_config": chat_config}, 
        stream=False
    )
    ans = ''
    decoder = codecs.getincrementaldecoder('utf-8')()
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            decoded = decoder.decode(chunk)
            ans += decoded
    ans += decoder.decode(b'', final=True)
    # {answer}[sp]{prompt}[q]\n\n{context}\n[ts]{timeStamp}[fema]{fema_add}

    answer = ans.split('[sp]')[0]
    context = ans.split('[ts]')[0].split('[q]')[1]

    return answer, context

# check results with context
def get_chatbot_response_with_context(prompt, context):
    messages = [
        {"role": "system", "content":[{"type": "text", "text": _system_prompts['qa']}]},
        {"role": "user", "content": [{"type": "text", "text": "Question: " + prompt + '\n\nContext: ' + context}]}
    ]

    response = _client['completion'].chat.completions.create(
        model=config['azure_openai_completion_deployment'],
        messages=messages,
        max_tokens=2048,
        temperature=0,  
        top_p=0.95,
        stop=None,  
        stream=False
    )

    # print(response.choices[0])
    answer = response.choices[0].message.content
    # print(context)

    return answer
