import json
import requests

zabbix_user = 'Admin'
zabbix_password = 'zabbix'
zabbix_url = 'http://192.168.23.202/zabbix/api_jsonrpc.php'

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

def getHostGroupID(host_group):
    group_id = ''
    user_token = getUserToken()
    data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            "name": [
                host_group
            ]
        }
    },
    "auth": user_token,
    "id": 2
    }
    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)
    try:
        group_id = json.loads(res.text).get('result')[0].get('groupid')
    except Exception:
        print('主机组不存在')
    if group_id:
        pass
    else:
        hostGroupAdd(groupname)
        group_id = getHostGroupID(groupname)
    # print(res.text)
    return group_id

def getTemplateID(template):
    user_token = getUserToken()
    data = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "extend",
        "filter": {
            "host": [
                template
            ]
        }
    },
    "auth": user_token,
    "id": 3
    }
    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)
    # print(res.text)
    template_id = json.loads(res.text).get('result')[0].get('templateid')
    return template_id

def hostGroupAdd(groupname):
    user_token = getUserToken()
    data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": groupname
    },
    "auth": user_token,
    "id": 4
    }
    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)

    if 'erron' in res.text:
        print('主机组添加失败')
    else:
        print('主机组添加成功')

def addNewHost(hostname,ip,groupname,template):
    user_token = getUserToken()
    group_id = getHostGroupID(groupname)
    template_id = getTemplateID(template)
    data = {
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": group_id
            }
        ],
        "templates": [
            {
                "templateid": template_id
            }
        ],
        "inventory_mode": 0
    },
    "auth": user_token,
    "id": 6
    }
    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)

    if 'error' in res.text:
        print('主机%s ip:%s添加失败' % (hostname,ip))
    else:
        print('主机%s ip:%s添加成功' % (hostname,ip))


if __name__ == '__main__':
    hostname = input('输入主机名:').strip()
    ip = input('输入主机ip:').strip()
    template = input('输入链接模板名:').strip()
    groupname = input('输入主机组:').strip()
    addNewHost(hostname=hostname,ip=ip,groupname=groupname,template=template)
    # a = getHostGroupID('my zabbix')
    # print(a)