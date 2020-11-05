import requests
import json

salt_login_url = "https://192.168.23.203:8888/login"
salt_url = "https://192.168.23.203:8888"

salt_user = "admin"
salt_pwd = "123"

requests.packages.urllib3.disable_warnings()

def getUserToken():
    data = {
        "username": salt_user,
        "password": salt_pwd,
        "eauth": "pam"
    }
    head = {"Content-Type":"application/json"}

    res = requests.post(url=salt_login_url,data=json.dumps(data),headers=head,verify=False)
    user_token = json.loads(res.text).get("return")[0].get("token")

    return user_token

def testPING():
    user_token = getUserToken()
    data = {
        "client": "local",
        "tgt": "*",
        "fun": "test.ping"
    }
    head = {"Content-Type":"application/json","X-Auth-Token":user_token}
    res = requests.post(url=salt_url,data=json.dumps(data),headers=head,verify=False)

    for ip,result in json.loads(res.text).get("return")[0].items():
        print("服务器%s测试通信结果：" % ip)
        print(result)
        print('------'*12)

def cmdRun():
    user_token = getUserToken()
    data = {
        "client":"local",
        "tgt":"*",
        "fun":"cmd.run",
        "arg":"uptime"
    }
    head = {"Content-Type":"application/json","X-Auth-Token":user_token}

    res = requests.post(url=salt_url,data=json.dumps(data),headers=head,verify=False)

    # print(res.text)

    for ip ,result in json.loads(res.text).get("return")[0].items():
        print("服务器%s执行uptime命令结果：" % ip)
        print(result)
        print('------' * 12)

if __name__ == '__main__':
    cmdRun()










