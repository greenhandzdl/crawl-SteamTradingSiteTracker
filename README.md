# 自动化数据抓取与解压脚本

本项目包含一个Python脚本，用于从指定的API下载文件，解压文件，并将数据整理到预定目录。脚本支持通过`.env`文件进行配置，包括API密钥和请求频率控制。

## 模块化结构

代码库采用模块化设计，将不同的功能分离到各自的文件中，以提高可维护性和可读性。项目结构如下：

```
.env.example
README.md
requirements.txt
pyproject.toml
src/
└── steam_tracker/
    ├── __init__.py
    ├── cli.py
    ├── core/
    │   ├── __init__.py
    │   └── api_client.py
    └── utils/
        ├── __init__.py
        └── config.py
```

- `src/steam_tracker/cli.py`: 脚本的主入口点，负责协调整个下载和解压过程。
- `src/steam_tracker/utils/config.py`: 负责从`.env`文件中加载和管理配置信息，如API参数和文件路径。
- `src/steam_tracker/core/api_client.py`: 封装了与API的所有交互，包括获取文件列表、下载文件、解压和清理。

## 安装

1. **克隆代码库:**

   ```bash
   git clone https://github.com/greenhandzdl/crawl-SteamTradingSiteTracker.git
   cd crawl-SteamTradingSiteTracker
   ```

2. **安装 `uv` (如果尚未安装):**

   ```bash
   pip install uv
   # 或者使用其他方式安装 uv
   ```

3. **创建并激活Python虚拟环境 (使用 `uv`):**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

4. **安装依赖 (使用 `uv`):**

   ```bash
   uv pip install -r requirements.txt
   ```

5. **安装项目为可编辑模式:**

   ```bash
   uv pip install -e .
   ```

## 配置

1. **创建`.env`文件:**

   复制`.env.example`文件来创建您的`.env`文件:

   ```bash
   cp .env.example .env
   ```

2. **编辑`.env`文件:**
   
   [阅读Readme](https://www.yuque.com/null_42/steam/glmytl66g4l4sufg)

   根据您的需求修改`.env`文件中的变量:

   - `TMP_OUTPUT_PATH`: 下载的临时文件存放路径 (默认为 `./temp`)。
   - `FILE_OUTPUT_PATH`: 解压后文件的存放路径 (默认为 `./output`)。
   - `REQUEST_PER_SECOND`: **请求频率限制**。每秒最大请求数，用于控制对API的访问频率，避免过载 (默认为 `3`)。
   - `DIR_NAME`: API需要的目标目录名。
   - `KEY`: (可选) API访问密钥。

## 使用

配置完成后，在激活虚拟环境的情况下，运行主脚本:

```bash
.venv/bin/python -m steam_tracker.cli
```

脚本将自动执行以下操作:

1. 从API获取文件列表。
2. 循环遍历文件列表，**逐个下载文件，并在下载完成后立即解压并删除临时压缩包**。

## [信息处理示例](https://github.com/greenhandzdl/analyse-data-SteamTradingSiteTracker)