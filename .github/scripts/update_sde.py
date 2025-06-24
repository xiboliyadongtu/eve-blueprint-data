import os
import yaml
import json
import zipfile
from urllib.request import urlretrieve

# ✅ 下载链接和路径设置
SDE_URL = "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
ZIP_PATH = "sde.zip"
EXTRACT_PATH = "sde"
BLUEPRINT_OUTPUT_DIR = "blueprints"
TYPENAME_OUTPUT_DIR = "typeNames"

# ✅ 清理旧数据
for path in [ZIP_PATH, EXTRACT_PATH, BLUEPRINT_OUTPUT_DIR, TYPENAME_OUTPUT_DIR]:
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.system(f"rm -rf {path}")

# ✅ 下载并解压
print("📥 下载 SDE 数据包...")
urlretrieve(SDE_URL, ZIP_PATH)

print("📦 解压缩文件...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_PATH)

# ✅ 自动查找包含 fsd/ 的子目录
fsd_root = None
for root, dirs, files in os.walk(EXTRACT_PATH):
    if 'fsd' in dirs:
        fsd_root = os.path.join(root, 'fsd')
        break

if not fsd_root:
    raise RuntimeError("❌ 未找到 fsd 目录，请检查解压结果")

# ✅ 创建输出目录
os.makedirs(BLUEPRINT_OUTPUT_DIR, exist_ok=True)
os.makedirs(TYPENAME_OUTPUT_DIR, exist_ok=True)

# ✅ 拆分 blueprints.yaml
print("🧩 拆分 blueprints.yaml...")
with open(os.path.join(fsd_root, "blueprints.yaml"), "r", encoding="utf-8") as f:
    blueprints_data = yaml.safe_load(f)

count_bp = 0
for blueprint in blueprints_data.values():
    if "activities" not in blueprint:
        continue
    typeID = blueprint.get("blueprintTypeID")
    data = {
        "activities": blueprint["activities"]
    }
    with open(f"{BLUEPRINT_OUTPUT_DIR}/{typeID}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    count_bp += 1

print(f"✅ 已导出 {count_bp} 个蓝图文件至 {BLUEPRINT_OUTPUT_DIR}/")

# ✅ 拆分 types.yaml
print("🧩 拆分 types.yaml...")
with open(os.path.join(fsd_root, "types.yaml"), "r", encoding="utf-8") as f:
    types_data = yaml.safe_load(f)

count_type = 0
for typeID, item in types_data.items():
    with open(f"{TYPENAME_OUTPUT_DIR}/{typeID}.json", "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False, indent=2)
    count_type += 1

print(f"✅ 已导出 {count_type} 个物品文件至 {TYPENAME_OUTPUT_DIR}/")
