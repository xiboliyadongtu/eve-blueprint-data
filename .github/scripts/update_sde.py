import os
import zipfile
import urllib.request
import yaml
import json

# ✅ 下载 EVE 官方 SDE ZIP 包
SDE_URL = "https://web.ccpgamescdn.com/aws/evesde/latest/sde.zip"
ZIP_PATH = "sde.zip"
EXTRACT_PATH = "sde"

# ✅ 清理旧文件
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
if os.path.exists(EXTRACT_PATH):
    import shutil
    shutil.rmtree(EXTRACT_PATH)

print("📦 Downloading SDE...")
urllib.request.urlretrieve(SDE_URL, ZIP_PATH)

print("📂 Extracting SDE...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_PATH)

# ✅ 拆分 blueprints.yaml
bp_path = os.path.join(EXTRACT_PATH, "sde/fsd/blueprints.yaml")
out_dir = "blueprints"
os.makedirs(out_dir, exist_ok=True)

print("🛠️ Splitting blueprints...")
with open(bp_path, "r", encoding="utf-8") as f:
    bps = yaml.safe_load(f)

for bp in bps:
    type_id = bp.get("blueprintTypeID")
    if type_id:
        with open(f"{out_dir}/{type_id}.json", "w", encoding="utf-8") as out:
            json.dump(bp, out, indent=2, ensure_ascii=False)

print(f"✅ Exported {len(bps)} blueprints to {out_dir}/")

# ✅ 拆分 types.yaml 为 typeID → 名称映射
type_path = os.path.join(EXTRACT_PATH, "sde/fsd/types.yaml")
type_out_dir = "typeNames"
os.makedirs(type_out_dir, exist_ok=True)

print("📑 Splitting typeNames...")
with open(type_path, "r", encoding="utf-8") as f:
    types = yaml.safe_load(f)

for t in types:
    type_id = t.get("typeID")
    if type_id:
        with open(f"{type_out_dir}/{type_id}.json", "w", encoding="utf-8") as out:
            json.dump(t, out, indent=2, ensure_ascii=False)

print(f"✅ Exported {len(types)} type names to {type_out_dir}/")
