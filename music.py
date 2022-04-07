"""
[知识点]：
    1.requests库的使用
    2.re正则表达式
    3.json字符串
    4.搜索歌曲爬取对应的音频文件

[开发环境]：
    1.python环境：annaconda5.2.0(python3.6.5)
    2.编辑器：pycharm
"""

import io
import re
import sys
import requests

sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}
keyword = sys.argv[1]
# keyword = "坂本龙一"
# keyword = input('请输入你想下载的歌曲名：')
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
params = {
    "ct": " 24",
    "qqmusic_ver": " 1298",
    "new_json": " 1",
    "remoteplace": " txt.yqq.song",
    "searchid": " 66595602585102401",
    "t": " 0",
    "aggr": " 1",
    "cr": " 1",
    "catZhida": " 1",
    "lossless": " 0",
    "flag_qc": " 0",
    "p": " 1",
    "n": " 15",
    "w": keyword,
    "g_tk_new_20200303": " 1390029147",
    "g_tk": " 1390029147",
    "loginUin": " 1164153961",
    "hostUin": " 0",
    "format": " json",
    "inCharset": " utf8",
    "outCharset": " utf-8",
    "notice": " 0",
    "platform": " yqq.json",
    "needNewCode": " 0"
}
response = requests.get(url, params=params, headers=headers)
# 正则表达式获取想要的json字符串，去除多余的
search_result = eval(re.findall('callback\((.*)\)', response.text)[0])
# 获取到data-song-list列表值
song_info = search_result['data']['song']['list']
songname = []
songmid = []
singer = []
# 循环获取songname，songmid，singer.name的值
for i in song_info:
    songname.append(i['songname'])
    songmid.append(i['songmid'])
    singer.append(i['singer'][0]['name'])
tplt = "{0:<10}\t{1:<10}\t{2:<20}"
# 标题输出
# print(tplt.format("序号", "歌手", "歌名"))
for i in range(len(songname)):
    # print(tplt.format(i, singer[i], songname[i]))
    songid = songmid[int(i)]
    url1 = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    params1 = {
        "-": "getplaysongvkey8636402145203543",
        "g_tk": "1390029147",
        "loginUin": "1164153961",
        "hostUin": "0",
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf-8",
        "notice": "0",
        "platform": "yqq.json",
        "needNewCode": "0",
        "data": '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"7469768631","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"7469768631","songmid":["' + songid + '"],"songtype":[0],"uin":"1164153961","loginflag":1,"platform":"20"}},"comm":{"uin":1164153961,"format":"json","ct":24,"cv":0}}'
    }
    response = requests.get(url1, params=params1, headers=headers)
    songlink = response.json()['req_0']['data']['midurlinfo'][0]['purl']
    if songlink == '':
        print(f"{'这首歌是付费歌曲无法下载'}")
    else:
        # with open(songname[i] + '.mp3', mode='wb') as f:
            # f.write(requests.get('https://isure.stream.qqmusic.qq.com/' + songlink, headers=headers).content)
            print(f"{songmid[i],songname[i],singer[i],'https://isure.stream.qqmusic.qq.com/'+ songlink}")
