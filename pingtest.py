import pandas as pd
import subprocess
import platform
import re

# 读取 CSV 文件
df = pd.read_csv('iplist.csv')

# 遍历每行，执行 ping 命令
for index, row in df.iterrows():
    desc = row['desc']
    ipv4 = row['ipv4']

    # 执行 ping 命令
    try:
        # 在 Windows 上，使用 'ping -n 1'，在 Linux/Mac 上，使用 'ping -c 1'
        command = f"ping -n 1 {ipv4}" if platform.system().lower() == 'windows' else f"ping -c 1 {ipv4}"
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, timeout=5)

        # 使用正则表达式提取延迟信息，针对不同格式进行匹配
        match = re.search(r"time=(\d+(\.\d+)?)\s?ms|(\d+(\.\d+)?)\s?ms\s+TTL=\d+", result.stdout)
        if match:
            latency = match.group(1) or match.group(3)
            print(f"{desc}: 延迟 {latency} ms")
        else:
            print(f"{desc}: 无法获取延迟信息")
    except subprocess.TimeoutExpired:
        print(f"{desc}: 延迟超时")
    except Exception as e:
        print(f"{desc}: 发生错误 - {e}")
