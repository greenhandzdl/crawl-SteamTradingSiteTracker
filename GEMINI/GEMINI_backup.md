我需要你完成一个`python`脚本，用于获取数据。
你需要：
0.获取.env文件的数据字段。
```
TMP_OUPUT_PATH=./tmp
FILE_OUTPUT_PATH=./output
REQUEST_PER_SECOND=2
DIR_NAME=priority_archive
KEY=
```
1.向`https://api.iflow.work/export/list?dir_name={DIR_NAME}`发送请求并尝试解析files所有参数。
```json

  "files": [
    "2024-02-13-00-15.zip",
    "2024-02-13-12-15.zip",
    ……
    "2025-10-27-12-15.zip"
  ],
  "success": true
}
```
2.读取files字段下所有内容，然后进行遍历获取。
构造链接`https://api.iflow.work/export/download?dir_name={DIR_NAME}&file_name=`，然后file_name替换为files字段下所有内容，然后下载到`TMP_OUPUT_PATH`目录下。
如果key存在，则构造链接类似于`https://api.iflow.work/export/download?dir_name=base_archive&file_name=2024-02-15-00-45.zip&key=ABC`
3.将获取每个`.zip`解压出所有内容到`FILE_OUTPUT_PATH`目录下，然后删除`.zip`文件。