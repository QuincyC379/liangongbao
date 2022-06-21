import random
import time
import sys
import requests
import json
from utils import single_user, random_ua, right_answer
from info import *


# 题库
tk_file_name = "answers.txt"

# 通过交互获得账号密码
user_info = single_user()

login_res = requests.post(login_url, headers=login_header, data=user_info).json()
print(login_res)
status = login_res.get("status")
debugger_file_name = f"lgb-debugger_{user_info['userName']}.json"

if status == 20000:
    token = login_res.get("data").get("token")
    memberId = login_res.get("data").get("memberId")
else:
    sys.exit('登录失败')

# 构造答题header
header['user-agent'] = random_ua()
header['token'] = login_res['data']['token']
header['memberId'] = login_res['data']['memberId']

# 获取第一道题
result = requests.post(startComp, headers=header, data={})
result_dict = result.json()
msg = result_dict.get("result").get("msg")
code = result_dict.get("result").get("code")

#写入文档
with open(debugger_file_name, "a", encoding="utf-8") as f:
    f.write(result.text + "\n")
# 已经答过了
if msg == "每天只能挑战一次哦~" and code == 9:
    print("每天只能挑战一次哦~")
    sys.exit()

# 
data = result_dict.get('data')
print(data)
quesId = data['ques']['quesId']
answerOptions = data['ques']['options']

while 1:
    rightAnswer = right_answer(result_dict)
    if rightAnswer:
        answer_data = {"quesId": f"{quesId}", "answerOptions": rightAnswer}
        print("rightAnswer", answer_data)
    else:
        # 题库没有答案时可以选择自己答题或者直接选择第一个选项

        # 自己答题
        user_answer = input('暂时没有答案，请输入答案选项数字以空格隔开：').split(' ')
        if data['ques']['quesTypeStr'] == '多选题':
            answer = [data['ques']['options'][int(i) - 1] for i in user_answer]
        else:
            answer = [data['ques']['options'][int(user_answer[0]) - 1]]
        answer_data = {"quesId": f"{quesId}", "answerOptions": answer}
        print("你的答案是:", answer)
        # 选第一个选项(用这个就把注释去掉)
        # data = {"quesId": f"{quesId}" , "answerOptions": [f"{answerOptions[0]}"]}
        # print("<--randomAnswer-->", answerOptions[0])

    # 答题之前等待时间
    time.sleep(random.randint(5, 9))
    answer_res = requests.post(answerQues, headers=header, data=json.dumps(answer_data))
    """
    {"result":{"msg":"成功"},"data":{"isRight":true,"answeredOptions":["对"],"ques":{"quesNo":2,"options":["保证工业生产的发展","保障生产经营单位财产安全","保障人民群众生命和财产安全"],"quesTypeStr":"单选题","quesId":"LChwai5EhnoUKCwA","content":"为了加强安全生产工作，防止和减少生产安全事故，（  ），促进经济社会持续健康发展，制定《安全生产法》。","quesType":1},"rightOptions":["对"]}}
    """
    print(answer_res.text)
    with open(debugger_file_name, "a", encoding="utf-8") as f:
        f.write(answer_res.text + "\n")
    result_dict = answer_res.json()
    data = result_dict.get("data")
    if data:
        ques = data.get("ques")
        if not ques:
            submit_comp = requests.post(
                submit_url, headers=header, data={}).json()
            resdata = submit_comp['data']
            print({'message': f'本次答对了{resdata["correctNum"]}题,得到了{resdata["score"]}分,获得称号:{resdata["labelTag"]},'})
            print("<------恭喜您，满分！！！------>")
            break
        else:
            quesId = ques.get("quesId")
            answerOptions = ques.get("options")
        # print("======程序执行结束======")
