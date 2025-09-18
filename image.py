import firebase_admin
from firebase_admin import storage, credentials, firestore
import uuid
import os

import summarize
import makeImage


def generate(name, path, image_text_list):
    bucket = storage.bucket()
    db = firestore.client()
    gen = {}

    for i, data in enumerate(image_text_list):
        file_path = data['image']  # 이미지 파일 경로
        text = data['text']  # 해당 이미지에 대한 텍스트

        random_uuid = uuid.uuid4()
        file_extension = os.path.splitext(file_path)[1]
        destination_blob_name = f'{random_uuid}{file_extension}'

        blob = bucket.blob(f"{name}/{destination_blob_name}")
        blob.upload_from_filename(file_path)

        gen[f'{i}'] = {
            'image': f"{destination_blob_name}",
            'text': text
        }

        print(f'File {file_path} uploaded to {destination_blob_name} with text "{text}".')

    # Firestore에 데이터 저장
    print({"generated": gen})
    doc_ref = db.collection("posts").document(path)
    doc_ref.set({"generated": gen}, merge=True)

if __name__ == '__main__':
    cred = credentials.Certificate(".env/serviceAccount.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {'storageBucket': 'edubook-7291e.appspot.com'})
    db = firestore.client()

    txt = "시오마라 카스트로 온두라스 대통령은 28일(현지시각) 소셜미디어에 “미국의 내정간섭, 미국이 대사관이나 다른 외교사절을 통해 온두라스 정치를 관리하려는 의도를 참을 수 없다”며 외교부에 범인인도조약의 종료를 지시했다고 밝혔다. 그는 이어 “그들은 주권 존중과 국민들의 자결, 불간섭, 보편적 평화를 규정하고 있는 국제법의 원칙과 관행을 공격하고 무시하고 위반했다. 이제 그만 됐다”고 적었다."

    name, image_text_list = makeImage.make_image(summarize.summarize(txt), "jangho")
    print(image_text_list)
    path = 'test'
    generate(name, path, image_text_list)
