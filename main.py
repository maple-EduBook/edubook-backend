import os
import time

import firebase_admin
import ocr
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from firebase_admin import credentials, firestore, storage
from image import generate
from makeImage import make_image
from model import GenerateReq
from summarize import summarize
from util import valid

load_dotenv(verbose=True, dotenv_path="./.env/.env")

cred = credentials.Certificate(".env/serviceAccount.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'edubook-7291e.appspot.com'})

db = firestore.client()

app = FastAPI(docs_url="/")


@app.post('/ping')
async def validate_token(request: Request):
    uid = valid.get_user_info_by_request(request)
    return uid


@app.post('/generate')
async def generate_image(request: Request, genReq: GenerateReq):
    uid = valid.get_user_info_by_request(request)['uid']
    doc_ref = db.collection("posts").document(genReq.post_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Document not found")

    time.sleep(5)

    img_name = doc.get("original")
    bucket = storage.bucket()
    blob = bucket.blob(f'{uid}/{img_name}')
    if not os.path.exists(f'./img/{uid}/'):
        os.makedirs(f'./img/{uid}/')
    blob.download_to_filename(f'./img/{uid}/{img_name}')

    # OCR

    # todo: ocr, debug
    # txt = "시오마라 카스트로 온두라스 대통령은 28일(현지시각) 소셜미디어에 “미국의 내정간섭, 미국이 대사관이나 다른 외교사절을 통해 온두라스 정치를 관리하려는 의도를 참을 수 없다”며 외교부에 범인인도조약의 종료를 지시했다고 밝혔다. 그는 이어 “그들은 주권 존중과 국민들의 자결, 불간섭, 보편적 평화를 규정하고 있는 국제법의 원칙과 관행을 공격하고 무시하고 위반했다. 이제 그만 됐다”고 적었다."
    # txt = "It was around the trun of the 20th century that Rosseaus's paintings began to attract some young artists. They were bored with exising painting styles and Rousseaus's paintings met their desire for a new trend. Especially, Pablo Picasso admired the strange energy of Rousseau's paintings because they looked unfamiliar and mysterious."

    ocr_img = ocr.img_ocr(f'./img/{uid}/{img_name}')
    summ_text = summarize(ocr_img)
    name, image_text_list = make_image(summ_text, uid)
    generate(name, genReq.post_id, image_text_list)
    return {"result": "success"}
