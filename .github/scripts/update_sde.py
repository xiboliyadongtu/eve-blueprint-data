
import os
import zipfile
import shutil
import yaml
import json
import urllib.request

# ✅ 下载 SDE 数据包（官方提供的 ZIP）
SDE_URL = "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
ZIP_PATH = "sde.zip"
LOCAL_PATH = "sde"

# 下载 ZIP 文件
urllib.request.urlretrieve(SDE_URL, ZIP_PATH)

# 解压 ZIP
if os.path.exists(LOCAL_PATH):
    shutil.rmtree(LOCAL_PATH)
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(LOCAL_PATH)

# 读取 YAML → 生成拆分 JSON
os.makedirs("blueprints", exist_ok=True)
os.makedirs("typeNames", exist_ok=True)

with open(f"{LOCAL_PATH}/fsd/blueprints.yaml", "r", encoding="utf-8") as f:
    blueprints = yaml.safe_load(f)
    for blueprint in blueprints:
        typeID = blueprint.get("blueprintTypeID")
        with open(f"blueprints/{typeID}.json", "w", encoding="utf-8") as out:
            json.dump(blueprint, out, ensure_ascii=False, indent=2)

print(f"✅ 拆分完成，共导出 {len(blueprints)} 个蓝图")

with open(f"{LOCAL_PATH}/fsd/types.yaml", "r", encoding="utf-8") as f:
    types = yaml.safe_load(f)
    for type_id, data in types.items():
        with open(f"typeNames/{type_id}.json", "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=2)

print(f"✅ 拆分完成，共导出 {len(types)} 个 typeID 名称文件")
