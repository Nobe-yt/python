import requests
import json
import pymysql
import sys

zabbix_user = 'Admin'
zabbix_password = 'zabbix'
zabbix_url = 'http://192.168.23.202/zabbix/api_jsonrpc.php'

def insertSQL2host_items_info(item_name,last_value,item_host_id):
    try:
        mysql_conn = pymysql.connect(host='192.168.23.202',user='admin',password='123',database='testdb')
    except Exception as e:
        print('数据库连接失败')
        print(e)
        sys.exit()
    cr = mysql_conn.cursor()

    insert_sql = "insert into host_items_info(item_name,last_value,item_host_id) values('%s','%s','%s')" % (item_name,last_value,item_host_id)
    cr.execute(insert_sql)

    mysql_conn.commit()

    cr.close()
    mysql_conn.close()


def insertSQL2hostinfo(host_name):
    try:
        mysql_conn = pymysql.connect(host='192.168.23.202', user='admin',password='123', database='testdb')
    except Exception as e:
        print('数据库连接失败')
        print(e)
        sys.exit()
    cr = mysql_conn.cursor()

    insert_sql = 'insert into hostinfo(hostname) values("%s")' % host_name
    cr.execute(insert_sql)

    mysql_conn.commit()

    cr.close()
    mysql_conn.close()

def sendPost(data):

    head = {'Content-Type':'application/json'}

    res = requests.post(url=zabbix_url,data=json.dumps(data),headers=head)

    return json.loads(res.text)
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
    user_token = sendPost(data=data).get('result')
    return user_token

def getALLHostInfo():
    host_info = {}
    user_token = getUserToken()
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend",
            "filter": {

            }
        },
        "auth": user_token,
        "id": 1
    }
    res = sendPost(data)
    for i in res.get('result'):
        insertSQL2hostinfo(i.get('host'))
        host_info[i.get('host')] = i.get('hostid')
    # print(host_info)
    return host_info
def getHostItemsInfo(hostids):

    user_token = getUserToken()
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostids,
            "sortfield": "name"
        },
        "auth": user_token,
        "id": 1
    }

    res = sendPost(data)
    for i in res.get('result'):
        insertSQL2host_items_info(item_name=i.get('name'),last_value=i.get('lastvalue'),item_host_id=i.get('hostid'))
        print('监控项:%s      当前值:%s' % (i.get('name'),i.get('lastvalue')))
    # print(res)

def getALLHostItemsInfo():
    all_host_info = getALLHostInfo()
    for host_name in all_host_info.keys():
        print('-----------主机: %s 的监控项信息如下： -------------' % host_name)
        getHostItemsInfo(all_host_info.get(host_name))
        print('********' * 15,end='\n\n')


if __name__ == '__main__':
    getALLHostItemsInfo()