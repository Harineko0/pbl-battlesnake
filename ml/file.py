import os
import re

def get_lastest_path(dir: str, pattern: str) -> tuple[str, int]:
    files = os.listdir(dir)

    # バージョン番号を抽出して、最大のバージョン番号を持つファイルを見つける
    latest_version = 0
    latest_file = None

    for file in files:
        match = re.match(pattern, file)
        if match:
            version = int(match.group(1))  # バージョン番号を整数として取得
            if version > latest_version:
                latest_version = version
                latest_file = file
    
    return latest_file, latest_version