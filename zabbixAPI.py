import requests
import json

zabbix_url = 'http://192.168.23.202/zabbix/api_jsonrpc.php'
zabbix_user = 'Admin'
zabbix_password = 'zabbix'

def getUserToken():
    data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": zabbix_user,
        "password": zabbix_password
    },
    "id": 1,
    }
    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)
    user_token = json.loads(res.text).get('result')
    return user_token

def getHostID():
    user_token = getUserToken()
    data = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": [
            "hostid",
            "host"
        ],
        "selectInterfaces": [
            "interfaceid",
            "ip"
        ]
    },
    "id": 2,
    "auth": user_token
    }
    head = {'Content-Type':'application/json'}
    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)
    print(res.text)
    host_id = json.loads(res.text).get('result')[0].get('hostid')
    interface_id = json.loads(res.text).get('result')[0].get('interfaces')[0].get('interfaceid')
    # print(host_id,interface_id)
    return host_id,interface_id

def itemCreate(disk_name):
    user_token = getUserToken()
    host_id,interface_id = getHostID()
    data = {
    "jsonrpc": "2.0",
    "method": "item.create",
    "params": {
        "name": "Free disk space on $1",
        "key_": "vfs.fs.size[%s,free]" % disk_name,
        "hostid": host_id,
        "type": 0,
        "value_type": 3,
        "interfaceid": interface_id,
        "delay": 30
    },
    "auth": user_token,
    "id": 3
    }
    head = {'Content-Type':'application/json'}
    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)
    # print(res.text)
    if 'error' in res.text:
        print('磁盘%s剩余空间监控创建失败' % disk_name)
    else:
        print('磁盘%s剩余空间监控创建成功' % disk_name)



if __name__ == '__main__':
    getHostID()