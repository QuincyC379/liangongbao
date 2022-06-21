import random
import time
import sys
import requests
import json
import re

# 题库
tk_file_name = "answers.txt"
token_url = "https://js.lgb360.com/lgb/user/loginByPassword.do"
token_header = {
    "token": "",
    "memberId": "",
    "mobileTerminal": "0",
    "appversion": "3.0.3",
    "User-Agent": "LGB/3.0.3 (HMA-AL00; Android 10; zh_CN_#Hans; e4802ed3-c836-4ba8-822c-51dc9cdac4f8; 3626613241)",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "js.lgb360.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# 写入自己的账号密码
token_data = {"userName": "xxxxxxxxxxx", "password": "1qaz2wsx!"}#t1

token_result = requests.post(token_url, headers=token_header, data=token_data)
token_dict = json.loads(token_result.text)
print(token_dict)
status = token_dict.get("status")
debugger_file_name = "lgb-debugger_%s.json" % token_data.get("userName")


def random_ua():
    ua_list = [
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 8.1; EML-AL00 Build/HUAWEIEML-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.143 Crosswalk/24.53.595.0 XWEB/358 MMWEBSDK/23 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.1.4.994 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/NON_NETWORK Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MHA-AL00 Build/HUAWEIMHA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.4.950 UWS/2.11.1.50 Mobile Safari/537.36 AliApp(DingTalk/4.5.8) com.alibaba.android.rimet/10380049 Channel/227200 language/zh-CN",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-AL00 Build/HUAWEIEML-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.13.1.48 Mobile Safari/537.36 AliApp(DingTalk/4.5.11) com.alibaba.android.rimet/10487439 Channel/227200 language/zh-CN",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; EML-TL00 Build/HUAWEIEML-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.14.0.13 Mobile Safari/537.36 AliApp(TB/7.10.4) UCBS/2.11.1.1 TTID/227200@taobao_android_7.10.4 WindVane/8.3.0 1080X2244",
        "Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; HUAWEI MT1-U06 Build/HuaweiMT1-U06) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 baiduboxapp/042_2.7.3_diordna_8021_027/IEWAUH_61_2.1.4_60U-1TM+IEWAUH/7300001a/91E050E40679F078E51FD06CD5BF0A43%7C544176010472968/1",
        "Mozilla/5.0 (Linux; Android 8.0; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/4G Language/zh_CN Process/tools",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.8.2 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.3.0 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B72c Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A421 wxwork/2.5.8 MicroMessenger/6.3.22 Language/zh",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 wxwork/2.5.1 MicroMessenger/6.3.22 Language/zh",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B100 Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baidubrowser/7.18.21.0 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.10 (Baidu; P1 6.0.1)",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; vivo Y85 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.6.976 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 5.1.1; OPPO R9 Plustm A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.12 baiduboxapp/10.12.0.12 (Baidu; P1 5.1.1)",
        "Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 7.1.1)",
        "Mozilla/5.0 (Linux; Android 5.1.1; vivo X6S A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044207 Mobile Safari/537.36 MicroMessenger/6.7.3.1340(0x26070332) NetType/4G Language/zh_CN Process/tools",
        "Mozilla/5.0 (Linux; Android 8.1.0; PACM00 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 7.1.1; vivo X20A Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.2.1340(0x2607023A) NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 8.1.0; vivo Y71A Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.2.2",
        "Mozilla/5.0 (Linux; Android 8.0.0; MI 6 Build/OPR1.170623.027; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)",
        "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MI 5 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.9.969 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 Maxthon/3235",
        "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Mi Note 3 Build/OPM1.171019.019) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.0.2",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 UWS/2.12.1.18 Mobile Safari/537.36 AliApp(TB/7.5.4) UCBS/2.11.1.1 WindVane/8.3.0 720X1280",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-N9500 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)",
    ]
    ua = random.choice(ua_list)
    return ua


if status == 20000:
    token = token_dict.get("data").get("token")
    memberId = token_dict.get("data").get("memberId")
ua_ = random_ua()
startComp = "https://aqy-app.lgb360.com/aqy/ques/startCompetition"
header = {
    "Host": "aqy-app.lgb360.com",
    "accept": "application/json, text/plain, */*",
    "token": "%s" % token,
    "user-agent": "%s" % ua_,
    "memberid": "%s" % memberId,
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://aqy-app.lgb360.com",
    "x-requested-with": "com.hxak.liangongbao",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}
result = requests.post(startComp, headers=header, data={})
result_dict = json.loads(result.text)
msg = result_dict.get("result").get("msg")
code = result_dict.get("result").get("code")
with open(debugger_file_name, "a", encoding="utf-8") as f:
    f.write(result.text + "\n")
if msg == "每天只能挑战一次哦~" and code == 9:
    print("每天只能挑战一次哦~")
    sys.exit()


def replace_file_answer(r_options, flags=0):
    text = '["FORTEST"]'
    filepath = "answers.txt"
    with open(filepath, "r+", encoding="utf-8") as f1:
        contents = f1.read()
        pattern = re.compile(re.escape(text), flags)
        contents = pattern.sub("%s" % json.dumps(r_options, ensure_ascii=False), contents)
        f1.seek(0)
        f1.truncate()
        f1.write(contents)


# def right_answer(json_dict, correct_answer):
def right_answer(json_dict):
    answer_ = ""
    content_ = ""
    if "data" in json_dict.keys():
        ques_ = json_dict.get("data").get("ques")
        content_ = ques_.get("content")
        with open(tk_file_name, "a+", encoding="utf-8") as f_:
            f_.seek(0)
            for lines_ in f_.readlines():
                if content_ in lines_:
                    ques_answer_ = lines_.strip("\n").split("######")
                    a = ques_answer_[1]
                    answer_ = json.loads(a)
            # if not answer_:
            #     f_.write(content_ + "######%s" % correct_answer + "\n")
    return answer_, content_


answerQues = "https://aqy-app.lgb360.com/aqy/ques/answerQues"
header = {
    "Host": "aqy-app.lgb360.com",
    "accept": "application/json, text/plain, */*",
    "token": "%s" % token,
    "user-agent": "%s" % ua_,
    "memberid": "%s" % memberId,
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://aqy-app.lgb360.com",
    "x-requested-with": "com.hxak.liangongbao",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"

}

while 1:
    data = result_dict.get("data")
    if data:
        ques = data.get("ques")
        if not ques:
            print("<------恭喜您，满分！！！------>")
            break
        else:
            quesId = ques.get("quesId")
            answerOptions = ques.get("options")
    else:
        points_url = "https://aqy-app.lgb360.com/aqy/regist/competition"
        points_header = {
            "Host": "aqy-app.lgb360.com",
            "accept": "application/json, text/plain, */*",
            "token": "%s" % token,
            "user-agent": "%s" % ua_,
            "memberid": "%s" % memberId,
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://aqy-app.lgb360.com",
            "x-requested-with": "com.hxak.liangongbao",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        # points = requests.get(points_url, headers=points_header)
        # points_dict = json.loads(points.text)
        # total_points = points_dict.get("data").get("points")
        # print("您当前的总积分为%s" % total_points)
        print("======程序执行结束======")
        break
    rightAnswer, cont = right_answer(result_dict)
    if rightAnswer:
        data = {"quesId": "%s" % quesId, "answerOptions": rightAnswer}
        print("rightAnswer", data)
    else:
        data = {"quesId": "%s" % quesId, "answerOptions": ["%s" % answerOptions[0]]}
        print("<--randomAnswer-->", answerOptions[0])
    answer = requests.post(answerQues, headers=header, data=json.dumps(data))
    print(answer.text)
    with open(debugger_file_name, "a", encoding="utf-8") as f:
        f.write(answer.text + "\n")
    result_dict = json.loads(answer.text)
    if "data" in result_dict.keys():
        d_ = result_dict.get("data")
        isRight = d_.get("isRight")
        if not isRight:
            with open(tk_file_name, "a", encoding="utf-8") as f:
                f.write(cont + "######%s" % '["FORTEST"]' + "\n")
            rightOptions = d_.get("rightOptions")
            replace_file_answer(rightOptions)
    time.sleep(random.randint(3, 6))
