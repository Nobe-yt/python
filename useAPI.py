import requests
import json

# res = requests.get(url='http://192.168.23.202')
# print(res)
# print(res.text)

head = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36'}
#
# res = requests.get(url='http://192.168.23.202',headers=head)
# print(res)
# print(res.text)
data = {'name':'Nobe','password':'123'}
res = requests.post(url='http://www.baidu.com',data=data,headers=head)
with open(r'D:\pycharmproject\testdir\html.txt',mode='wb') as f:
    f.write(res.text.encode('utf-8'))
# print(res.text)

# data = {'a':1,'b':2}
# data1 = '{"a":1,"b":2}'
# new_data = json.dumps(data)
# print(type(data))
#
# new_data1 = json.loads(data1)
# print(type(new_data1))



