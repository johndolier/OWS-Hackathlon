
# MOSAIC_ENDPOINT = 'https://qnode.eu/ows/mosaic/service/'
MOSAIC_ENDPOINT = "http://mosaic:8008/"

import requests
import json


def make_web_query(query:str, limit:int = 10, index=None) -> list[dict]:
    print(f"make web search request to endpoint {MOSAIC_ENDPOINT}")
    print(f"Query: {query}, Limit: {limit}")
    if index is None:  
      request_url = f"{MOSAIC_ENDPOINT}search?q={query}&limit={limit}"
    else:
      # todo use specific index
      request_url = ""

    print(f"Request URL: {request_url}")
    response = requests.get(request_url)
    try:
        response_dict = json.loads(response.text)
    except Exception as e:
        print(f"Exception in parsing response - {e}")
        print(f"Status code: {response.status_code}")
        response_dict = {}

    results = response_dict.get('results', [])
    if not results:
        return []

    # TODO data post processing
    id_list = []
    for result in results:
       for index, document_list in result.items():
        #   print(f"Index: {index}")
        #   print(f"Found {len(document_list)} documents")
          for document in document_list:
              id = document.get('id', None)
              if id is not None:
                  id_list.append(id)

    
    full_text_dict = get_full_text_dict(id_list)

    return full_text_dict


def get_full_text(id):
    request = f"{MOSAIC_ENDPOINT}full-text?id={id}"
    response = requests.get(request)
    response_dict = {}
    try: 
        response_dict = json.loads(response.text)
    except Exception as e:
        print(f"Exception in parsing response - {e}")
        print(f"Status code: {response.status_code}")
    
    return response_dict['fullText']


def get_full_text_dict(id_list):
    print(f'Documents: {len(id_list)}')
    full_text_dict = {}
    for id in id_list:
        print(f"Get full text for document with id {id}")
        full_text_dict[id] = get_full_text(id)
    return full_text_dict
  

   
