import requests
import pandas as pd
import json

# 发送 HTTP 请求获取 JSON 数据，禁用 SSL 证书验证
url = 'https://api.steampowered.com/ISteamApps/GetSDRConfig/v1?appid=730'
response = requests.get(url, verify=False)

# 检查请求是否成功
if response.status_code == 200:
    # 将 JSON 数据保存为 sdr.json 文件
    with open('sdr.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)
    print("API 响应已保存为 sdr.json 文件。")

    # 读取 JSON 文件并创建 DataFrame
    with open('sdr.json', 'r') as json_file:
        data = []
        dic = json.load(json_file)
        for city, city_info in dic['pops'].items():
            desc = city_info['desc']
            relays = city_info.get('relays', [])
            for relay in relays:
                ipv4 = relay['ipv4']
                data.append([desc, ipv4])

    # 创建 Pandas DataFrame
    df = pd.DataFrame(data, columns=['desc', 'ipv4'])

    # 显示 DataFrame
    print(df)

    # 保存 DataFrame 为 CSV 文件
    df.to_csv('iplist.csv', index=False)
    print("DataFrame 已保存为 iplist.csv")
else:
    print(f"错误：无法获取数据。状态码：{response.status_code}")
