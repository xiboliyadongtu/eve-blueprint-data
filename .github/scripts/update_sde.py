import os
import shutil
import yaml
import json
import subprocess

SDE_REPO = "https://github.com/ccpgames/eve-static-data-export.git"
LOCAL_PATH = "sde"
BLUEPRINT_OUT = "blueprints"
TYPENAME_OUT = "typeNames"

# 克隆或更新仓库
if os.path.exists(LOCAL_PATH):
    shutil.rmtree(LOCAL_PATH)
subprocess.run(["git", "clone", "--depth", "1", SDE_REPO, LOCAL_PATH])

# 加载并拆分蓝图
with open(f"{LOCAL_PATH}/fsd/blueprints.yaml", "r", encoding="utf-8") as f:
    bps = yaml.safe_load(f)

os.makedirs(BLUEPRINT_OUT, exist_ok=True)
for bp in bps:
    tid = bp["blueprintTypeID"]
    with open(f"{BLUEPRINT_OUT}/{tid}.json", "w", encoding="utf-8") as out:
        json.dump(bp, out, indent=2)

# 加载并拆分类型名
with open(f"{LOCAL_PATH}/fsd/types.yaml", "r", encoding="utf-8") as f:
    types = yaml.safe_load(f)

os.makedirs(TYPENAME_OUT, exist_ok=True)
for tid, entry in types.items():
    with open(f"{TYPENAME_OUT}/{tid}.json", "w", encoding="utf-8") as out:
        json.dump(entry, out, indent=2)
