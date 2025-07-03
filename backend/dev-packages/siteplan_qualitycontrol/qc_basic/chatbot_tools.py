"""
Script containing function to communicate with the Chatbot.
"""

import requests
from requests.exceptions import ConnectionError
# city, zone, prompt, tool_use
def get_chatbot_response(zone='(C-1)', prompt='Allowed building height?', tool_use = True ,  url='http://192.168.1.223:5000/rag_predict'):
    print(zone)
    data = {'zone': zone,'prompt': prompt, 'tool_use':tool_use, 'chat_type_request':"Zoning"}
    response = requests.post(url, json=data, stream=True)
    result = ''
    if response.status_code == 200:
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                if '[sp]' in chunk:
                    result+=chunk.split('[sp]')[0]
                    break
                else:
                    result+=chunk
    else:
        result = f"Failed to fetch data. Status code: {response.status_code}"
    return result


# import requests
# from requests.exceptions import ConnectionError
 
def check_api_connection(url='http://192.168.1.223:5000/rag_predict', time_out=0.5):
    try:
        r = requests.get(url, timeout=time_out)
        if r.status_code!=200 and r.status_code!=405:
            return 'Connection Error'
    except ConnectionError as e:    # This is the correct syntax
        return 'Connection Error'
    return 'Connection Established'