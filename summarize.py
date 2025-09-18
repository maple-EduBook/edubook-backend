import os
import re
from dotenv import load_dotenv
from openai import OpenAI
import ocr
import json

load_dotenv(verbose=True,dotenv_path="./.env/.env")
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def summarize(txt, model="gpt-3.5-turbo", temperature=0.1):
    prompt = """
       You are an assistant helping students with textbook summaries. You will be given a fingerprint from a textbook, and your task is to summarize the fingerprint in four parts, each in **Korean**. Output your response in JSON format with the following structure:

        {
          "answer1": "Summary of the first key point from the fingerprint in Korean.",
          "answer2": "Summary of the second key point in Korean.",
          "answer3": "Summary of the third key point in Korean.",
          "answer4": "Summary of the fourth key point in Korean."
        }
        
        Ensure that each summary focuses on a distinct aspect of the fingerprint provided and that the text is written in Korean.
    """

    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": txt + "\n" + prompt}],
        temperature=temperature
    ) 
    summ = res.choices[0].message.content

    # 'Part' 레이블과 불필요한 줄바꿈을 제거하고 정리
    print(summ)
    clean_summary = remove_part_labels(summ)


    # 결과를 개별 부분으로 나누기
    # parts = re.split(r'(?<=\.) (?=\S)', clean_summary)

    part1 = clean_summary[0]
    part2 = clean_summary[1]
    part3 = clean_summary[2]
    part4 = clean_summary[3]

    # Optional: You can further split each part by sentences, for example, if that's needed:
    part1_sentences = re.split(r"(?<=\.) (?=\S)", part1)
    part2_sentences = re.split(r"(?<=\.) (?=\S)", part2)
    part3_sentences = re.split(r"(?<=\.) (?=\S)", part3)
    part4_sentences = re.split(r"(?<=\.) (?=\S)", part4)

    # Put the parts into a list (you can put sentences or raw parts as per your need)
    parts_list = [part1_sentences, part2_sentences, part3_sentences, part4_sentences]

    return_li = []
    for i in parts_list:
        for j in i:
            return_li.append(j)

    return return_li

def remove_part_labels(text):
    # Convert JSON string to Python dictionary
    dictionary = json.loads(text)
    return list(dictionary.values())

if __name__ == '__main__':
    # txt = "시오마라 카스트로 온두라스 대통령은 28일(현지시각) 소셜미디어에 “미국의 내정간섭, 미국이 대사관이나 다른 외교사절을 통해 온두라스 정치를 관리하려는 의도를 참을 수 없다”며 외교부에 범인인도조약의 종료를 지시했다고 밝혔다. 그는 이어 “그들은 주권 존중과 국민들의 자결, 불간섭, 보편적 평화를 규정하고 있는 국제법의 원칙과 관행을 공격하고 무시하고 위반했다. 이제 그만 됐다”고 적었다."

    # print(summarize(ocr.img_ocr('./img/english.jpg')))
    summary = summarize(ocr.img_ocr('./img/english.jpg'))
    print(summary)
    print(type(summary))