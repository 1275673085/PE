import requests
import os

# 基础URL
base_url = "https://api.dandiarchive.org/"

# 数据集的ID和版本
dandiset_id = "000055"
version = "0.220127.0436"

# 要保存文件的目录
save_dir = "/home/weichen/projects/shiyin/PE/data/AJILE12"  

# 获取资产列表的URL
assets_url = f"{base_url}api/dandisets/{dandiset_id}/versions/{version}/assets/"

# 发送请求获取资产列表
response = requests.get(assets_url)
assets = response.json()['results']

# 检查保存目录是否存在，如果不存在，则创建
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 遍历资产并下载
for asset in assets:
    asset_id = asset['asset_id']
    file_name = asset['path'].split('/')[-1]
    download_url = f"{base_url}api/assets/{asset_id}/download/"

    # 发送请求下载文件
    r = requests.get(download_url)
    file_path = os.path.join(save_dir, file_name)

    # 保存文件
    with open(file_path, 'wb') as f:
        f.write(r.content)
    print(f"Downloaded {file_name}")

print("All files downloaded successfully.")
