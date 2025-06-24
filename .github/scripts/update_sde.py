import os, json, yaml, shutil
from urllib.request import urlretrieve
from zipfile import ZipFile

# 下载 SDE
sde_url = "https://developers.eveonline.com/resource/sde/latest"
zip_path = "/tmp/sde.zip"
sde_dir = "/tmp/sde"
urlretrieve(sde_url, zip_path)

# 解压
with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(sde_dir)

fsd_dir = os.path.join(sde_dir, "fsd")
bp_yaml = os.path.join(fsd_dir, "blueprints.yaml")
type_yaml = os.path.join(fsd_dir, "types.yaml")

# 拆分蓝图
with open(bp_yaml, "r", encoding="utf-8") as f:
    blueprints = yaml.safe_load(f)

os.makedirs("blueprints", exist_ok=True)
bp_index = []
for bp_id, data in blueprints.items():
    with open(f"blueprints/{bp_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    bp_index.append(bp_id)

with open("blueprints/index.json", "w") as f:
    json.dump(bp_index, f)

# 拆分 typeNames
with open(type_yaml, "r", encoding="utf-8") as f:
    types = yaml.safe_load(f)

os.makedirs("typeNames", exist_ok=True)
tn_index = []
for entry in types:
    tid = entry.get("typeID")
    name = entry.get("name", {})
    volume = entry.get("volume")
    if tid:
        with open(f"typeNames/{tid}.json", "w", encoding="utf-8") as f:
            json.dump({"id": tid, "name": name, "volume": volume}, f, ensure_ascii=False)
        tn_index.append({"id": tid, "name": name})

with open("typeNames/index.json", "w") as f:
    json.dump(tn_index, f)

print("✅ Auto update complete.")
