# MMAC-Copilot



### Introduction



### Installation

1. Clone the repository

2. To install the main part of the project, we suggest to create a new conda environment. 

```sh
conda create -n MMAC python=3.10 -y
conda activate MMAC

pip install -r requirements.txt
pip install langchain_openai
```

3. After installation, please set several environment variables from different services. To apply for Bing API, please refer to document [Apply BING_Search_API_Key](https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource).

```sh
cp .env.sample .env
```

4. For starting vision module services, we need to install according to following commands:

```sh
cd vision/VisionServer
conda create -n MMAC_Vision python=3.10 -y
conda activate MMAC_Vision

pip install -r requirements.txt
```



### Running the project

1. If you need to use API services and vision API, please start:

```sh
python -m friday.core.api_server &

cd vision/VisionServer && python server.py &
```

2. Run MMAC-Copilot

```bash
python run.py [OPTIONS]
```

**Options**

- `--action_lib_path`
  - **Default**: `'friday/action_lib'`
  - **Description**: Path to store/load the tool repository.
  
- `--config_path`
  - **Default**: `'.env'`
  - **Description**: Path to env config file.

- `--query`
  - **Default**: `"I want to open google chrome browser, and use vision actions to search Friends Series"`
  - **Description**: The task command to execute.
  
- `--query_file_path`
  - **Default**: empty
  - **Description**: Path to a file containing task instructions (optional).
  
- `--logging_filedir`
  - **Default**: `'log'`
  - **Description**: Directory for log files.
  
- `--logging_filename`
  - **Default**: `'temp.log'`
  - **Description**: Log file name.
  
- `--logging_prefix`
  - **Default**: Random 4-character string
  - **Description**: Prefix for log file names.
  
- `--score`
  - **Default**: `8`
  - **Description**: Critic score threshold for storing the actions

**Example Usage**

```bash
python run.py --query "Help me open Spotify and play a song." --score 6
```