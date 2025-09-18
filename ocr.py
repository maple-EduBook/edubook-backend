import os
import requests
import uuid
import time
import json
from dotenv import load_dotenv

load_dotenv(verbose=True,dotenv_path="./.env/.env")
secret_key =os.getenv('OCR_SECRET_KEY')

load_dotenv(verbose=True,dotenv_path="./.env/.env")
api_url =os.getenv('API_URL')


def img_ocr(img_file : str):
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
      ('file', open(img_file,'rb'))
    ]
    headers = {
      'X-OCR-SECRET': secret_key
    }

    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
    ocr_res = json.loads(response.text)

    all_text = []
    for i in ocr_res['images']:
        for j in i['fields']:
            text = j['inferText']
            all_text.append(text)
    full_text = ' '.join(all_text)

    print(full_text)
    return full_text

if __name__ == "__main__":
   print(img_ocr('img/english.jpg'))