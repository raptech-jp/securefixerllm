import os.path
import urllib.request
import urllib.parse

base_url = "https://cve.mitre.org/"
path = "cgi-bin/cvekey.cgi"
headers = {
    "Accept-Language": "ja_JP",
}
query = {
    "keyword": "openai"
}

# os.pathを使ってURLを結合
url = os.path.join(base_url, path)

# クエリストリング
url_with_query = "{}?{}".format(url, urllib.parse.urlencode(query))

print(url_with_query)
req = urllib.request.Request(url_with_query, headers=headers)

# tryでエラーハンドリング
try:
    with urllib.request.urlopen(req) as res:
        body = res.read().decode("utf-8")
        print(body)

except urllib.error.HTTPError as e:
    # Status codeでエラーハンドリング
    if e.code >= 400:
        print(e.reason)
    else:
        raise e