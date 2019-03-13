import json
import urllib.request
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException

config_file_patch = os.path.dirname(__file__) + '/config.json'
with open(config_file_patch) as file:
    config = json.loads(file.read())

client = AcsClient(config['AccessKeyID'], config['AccessKeySecret'], 'default')

def get_common_request():
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('alidns.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2015-01-09')
    return request

# 获得域名解析列表
def get_all_record():
    request = get_common_request()
    request.set_action_name('DescribeDomainRecords')
    request.add_query_param('DomainName', 'linshangyao.cn')

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    return response


# 修改域名解析记录
def update_domain_record(rr: str):
    request = get_common_request()

    request.set_action_name('UpdateDomainRecord')
    record_id = get_record_id(rr)

    request.add_query_param('RecordId', record_id)
    request.add_query_param('RR', rr)
    request.add_query_param('Type', 'A')
    request.add_query_param('Value', get_public_ip())
    request.add_query_param('TTL', '600')
    try:
        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
    except ServerException as e:
        err_code =e.get_error_code()
        if 'DomainRecordDuplicate' == err_code:
            print('dup')
        else:
            raise e

def get_record_id(rr: str):
    all_record_resp = json.loads(get_all_record().decode('utf-8'))
    records = all_record_resp["DomainRecords"]["Record"]
    for each in records:
        if each["RR"] == rr:
            return each["RecordId"]

def get_public_ip():
    url = "https://api.ipify.org/?format=json"
    response = urllib.request.urlopen(url)
    jsonstr = response.read().decode()
    return json.loads(jsonstr)['ip']

update_domain_record(config['Domain'])


