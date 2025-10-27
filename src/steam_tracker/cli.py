from steam_tracker.utils.config import DIR_NAME
from steam_tracker.core.api_client import get_file_list, download_files

def main():
    if not DIR_NAME:
        print("错误: DIR_NAME 未在 .env 文件中设置.")
    else:
        files = get_file_list()
        if files:
            download_files(files)
            print("所有操作完成.")

if __name__ == "__main__":
    main()