
import requests
import time
import os
import zipfile
from steam_tracker.utils.config import DIR_NAME, KEY, TMP_OUPUT_PATH, REQUEST_PER_SECOND, FILE_OUTPUT_PATH

def get_file_list():
    """获取文件列表"""
    api_url = f"https://api.iflow.work/export/list?dir_name={DIR_NAME}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if data.get("success") and "files" in data:
            return data["files"]
        else:
            print(f"获取文件列表失败: {data.get('message', data)}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"请求文件列表时发生错误: {e}")
        return []

def download_files(file_list):
    """下载文件，并立即解压和清理"""
    os.makedirs(TMP_OUPUT_PATH, exist_ok=True)
    os.makedirs(FILE_OUTPUT_PATH, exist_ok=True)
    for file_name in file_list:
        download_url = f"https://api.iflow.work/export/download?dir_name={DIR_NAME}&file_name={file_name}"
        if KEY:
            download_url += f"&key={KEY}"

        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            file_path = os.path.join(TMP_OUPUT_PATH, file_name)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"文件 {file_name} 下载成功.")

            # 解压并清理
            if file_name.endswith(".zip"):
                try:
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(FILE_OUTPUT_PATH)
                    print(f"文件 {file_name} 解压成功.")
                    os.remove(file_path)
                    print(f"临时文件 {file_name} 已删除.")
                except zipfile.BadZipFile:
                    print(f"文件 {file_name} 不是一个有效的zip文件.")
                except Exception as e:
                    print(f"处理文件 {file_name} 时发生错误: {e}")
            else:
                print(f"文件 {file_name} 不是zip文件，跳过解压.")

            time.sleep(1 / REQUEST_PER_SECOND)

        except requests.exceptions.RequestException as e:
            print(f"下载文件 {file_name} 时发生错误: {e}")
