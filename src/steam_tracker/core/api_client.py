
import requests
import time
import os
import zipfile
import threading
import concurrent.futures
from steam_tracker.utils.config import DIR_NAME, KEY, TMP_OUTPUT_PATH, REQUEST_PER_SECOND, FILE_OUTPUT_PATH

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
    os.makedirs(TMP_OUTPUT_PATH, exist_ok=True)
    os.makedirs(FILE_OUTPUT_PATH, exist_ok=True)

    # 确保请求速率是正整数
    try:
        rate = max(1, int(REQUEST_PER_SECOND))
    except Exception:
        rate = 1

    # 简单的令牌桶限速器：每秒重置为 rate 个 token
    class RateLimiter:
        def __init__(self, rate_per_sec: int):
            self.rate = rate_per_sec
            self.tokens = rate_per_sec
            self.cond = threading.Condition()
            t = threading.Thread(target=self._refill_daemon, daemon=True)
            t.start()

        def _refill_daemon(self):
            while True:
                time.sleep(1)
                with self.cond:
                    self.tokens = self.rate
                    self.cond.notify_all()

        def acquire(self):
            with self.cond:
                while self.tokens <= 0:
                    self.cond.wait()
                self.tokens -= 1

    limiter = RateLimiter(rate)

    def _download_worker(file_name: str):
        # 在发起请求前先获取一个令牌
        limiter.acquire()

        download_url = f"https://api.iflow.work/export/download?dir_name={DIR_NAME}&file_name={file_name}"
        if KEY:
            download_url += f"&key={KEY}"

        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            file_path = os.path.join(TMP_OUTPUT_PATH, file_name)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
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

        except requests.exceptions.RequestException as e:
            print(f"下载文件 {file_name} 时发生错误: {e}")

    # 使用线程池并发下载。max_workers 取决于 file_list 长度与 rate。
    max_workers = min(max(2, rate * 2), len(file_list) or 1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = [exe.submit(_download_worker, fn) for fn in file_list]
        # 等待所有任务完成并传播异常（如有）
        for fut in concurrent.futures.as_completed(futures):
            try:
                fut.result()
            except Exception as e:
                # 已经在 worker 内打印错误信息，这里仅做额外记录
                print(f"下载任务出现异常: {e}")
