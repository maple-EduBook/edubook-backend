import base64
import os
import uuid
import requests
from dotenv import load_dotenv
import openai
from ocr import img_ocr
from summarize import summarize

load_dotenv(verbose=True,dotenv_path="./.env/.env")
stability_api_key =os.getenv('STABILITY_AI_KEY')
load_dotenv(verbose=True,dotenv_path="./.env/.env")
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

invoke_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
headers = {
    "Authorization": f"Bearer {stability_api_key}",
    "Accept": "application/json",
}

def translate_ko(txt, model="gpt-3.5-turbo", temperature=0.1):
    prompt = f"""
    번역해 주세요:
    한국어: {txt}
    영어로 번역된 내용:
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    translated_text = response.choices[0].message.content
    return translated_text

def make_image(prompt_list : list, username : str):

    image_text_list = []

    for prompt in prompt_list:
        tran_str = translate_ko(prompt)  # 텍스트 번역
        payload = {
            "text_prompts": [
                {"text": f"{tran_str}", "weight": 1},
            ],
            "cfg_scale": 7,
            "sampler": "K_DPM_2_ANCESTRAL",
            "seed": 0,
            "steps": 25
        }

        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        response_body = response.json()
        base64_string = response_body['artifacts'][0]['base64']

        image_path = save_image(base64_string, username)
        image_text_list.append({'image': image_path, 'text': prompt})

    print(f"All images saved in {username}")
    return username, image_text_list

def save_image(base_64, username):

    image_data = base64.b64decode(base_64)

    folder_path = os.path.join("img", username)

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_uuid = uuid.uuid4()
    file_name = f"{file_uuid}.jpg"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "wb") as f:
        f.write(image_data)

    print(f"Image successfully saved to {file_path}")
    return file_path

if __name__ == '__main__':
    img = img_ocr("./img/history.jpg")
    summ = summarize(img)
    print(summ)

    username, image_text_list = make_image(summ,"jangho")
    print(f"Folder name: {username}")
    print("Image and Text List:")
    for item in image_text_list:
        print(item)




# ---- ver. v2 Stable Image Core Code ----

# import base64
# import os
# import uuid
# import requests
# from dotenv import load_dotenv
# import openai
#
# # Load environment variables
# load_dotenv(verbose=True, dotenv_path="./.env/.env")
# api_key = os.getenv('OPENAI_API_KEY')
# stability_api_key = os.getenv('STABILITY_AI_KEY')
# client = openai.OpenAI(api_key=api_key)
#
# # Stability.ai API URL
# invoke_url = "https://api.stability.ai/v2beta/stable-image/generate/core"
#
# # Request headers
# headers = {
#     "authorization": f"Bearer {stability_api_key}",
#     "accept": "application/json;type=image/png",
# }
#
# def translate_ko(txt, model="gpt-3.5-turbo", temperature=0.1):
#     prompt = f"""
#     번역해 주세요:
#     한국어: {txt}
#     영어로 번역된 내용:
#     """
#     response = openai.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=temperature
#     )
#     translated_text = response.choices[0].message.content
#     return translated_text
#
# def make_image(prompt_list: list, username: str):
#     image_text_list = []
#
#     for prompt in prompt_list:
#         tran_str = translate_ko(prompt)  # Translate text to English
#         payload = {
#             "prompt": tran_str,
#             "style_preset": "comic-book",
#         }
#
#         response = requests.post(invoke_url, headers=headers, data=payload, files={"none": ''})
#         response.raise_for_status()
#         response_body = response.json()
#
#         base64_string = response_body['image']
#
#         image_path = save_image(base64_string, username)
#         image_text_list.append({'image': image_path, 'text': prompt})
#
#     print(f"All images saved in {username}")
#     return username, image_text_list
#
# def save_image(base_64, username):
#     image_data = base64.b64decode(base_64)
#
#     folder_path = os.path.join("img", username)
#
#     # Create folder if it doesn't exist
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#
#     file_uuid = uuid.uuid4()
#     file_name = f"{file_uuid}.jpg"
#     file_path = os.path.join(folder_path, file_name)
#
#     with open(file_path, "wb") as f:
#         f.write(image_data)
#
#     print(f"Image successfully saved to {file_path}")
#     return file_path
#
# if __name__ == '__main__':
#     username, image_text_list = make_image([
#         '시오마라 카스트로 온두라스 대통령은 미국의 내정간섭을 비판하며 외교부에 범인인도조약의 종료를 지시했다.',
#         '온두라스 대통령은 미국이 대사관이나 다른 외교사절을 통해 온두라스 정치를 관리하려는 의도를 비판하고, 주권 존중과 국민들의 자결을 강조했다.',
#         '대통령은 미국의 행동이 국제법의 원칙과 관행을 공격하고 무시하며 위반했다고 지적하며, 이를 더 이상 용납할 수 없다고 밝혔다.',
#         '시오마라 카스트로 대통령은 미국의 행동을 비판하고, 미국의 온두라스 정치에 대한 개입을 중단할 것을 촉구하며, 국제법의 원칙을 존중하라고 요구했다.'
#     ], "jangho")
#     print(f"Folder name: {username}")
#     print("Image and Text List:")
#     for item in image_text_list:
#         print(item)
