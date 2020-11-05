import requests
import sys
import json

requests.packages.urllib3.disable_warnings()

class SaltAPI():
    def __init__(self,salt_url,salt_user,salt_pwd):
        self.salt_url = salt_url
        self.salt_user = salt_user
        self.salt_pwd = salt_pwd
        if salt_url.endswith('/'):
            self.salt_url_login = salt_url + 'login'
        else:
            self.salt_url_login = salt_url + '/login'

    def __getUserToken(self):
        head = {'Content-Type':'application/json'}
        data = {
            "username": self.salt_user,
            "password": self.salt_pwd,
            "eauth":"pam"
        }
        res = requests.post(url=self.salt_url_login,data=json.dumps(data),headers=head,verify=False)

        user_token = json.loads(res.text).get("return")[0].get("token")
        head["X-Auth_Token"] = user_token
        return head
    def testPING(self,minion_id):
        head = self.__getUserToken()
        data = {
            "client":"local",
            "tgt":minion_id,
            "fun":"test.ping"
        }
        res = requests.post(url=self.salt_url,data=json.dumps(data),headers=head,verify=False)
        for ip ,result in json.loads(res.text).get("return")[0].items():
            print("服务器%s测试通信结果:" % ip)
            print(result)
            print('-------'*10)

    def cmdRUN(self,minion_id,cmd):
        head = self.__getUserToken()
        data = {
            "client":"local",
            "tgt":minion_id,
            "fun":"cmd.run",
            "arg":cmd
        }
        res = requests.post(url=self.salt_url,data=json.dumps(data),headers=head,verify=False)
        for ip ,result in json.loads(res.text).get("return")[0].items():
            print("服务器%s执行命令%s结果:" % (ip,cmd))
            print(result)
            print('-------'*10)

    def serviceControl(self,minion_id,service_name,service_op):
        head = self.__getUserToken()
        data = {
            "client":"local",
            "tgt":minion_id,
            "fun":"service.%s" % service_op,
            "arg":service_name
        }
        res = requests.post(url=self.salt_url,data=json.dumps(data),headers=head,verify=False)
        for ip ,result in json.loads(res.text).get("return")[0].items():
            if result:
                print('服务器%s %s %s 成功' % (ip,service_op,service_name))
            else:
                print('服务器%s %s %s 失败' % (ip, service_op, service_name))

    def pkgInstall(self,*args,minion_id,pkg_op):
        head = self.__getUserToken()
        for i in args:
            data = {
                "client": "local",
                "tgt": minion_id,
                "fun": "pkg.%s" % pkg_op,
                "arg": i
            }
            res = requests.post(url=self.salt_url,data=json.dumps(data),headers=head,verify=False)
            for ip ,result in json.loads(res.text).get("return")[0].items():
                if result:
                    print('服务器%s %s %s 成功' % (ip, pkg_op, i))
                else:
                    print('服务器%s %s %s 失败' % (ip, pkg_op, i))


if __name__ == '__main__':
    p1 = SaltAPI(salt_url='https://192.168.23.203:8888',salt_user='admin',salt_pwd='123')
    # p1.testPING(minion_id=''*')
    # p1.cmdRUN(minion_id='192.168.23.203',cmd='free -m')
    # p1.serviceControl(minion_id='*',service_name='mariadb',service_op='start')
    p1.pkgInstall(minion_id='192.168.23.204',pkg_op='remove',*('httpd','vsftpd'))