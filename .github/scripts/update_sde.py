import os
import zipfile
import yaml
import json
import shutil
from urllib.request import urlretrieve
from git import Repo

SDE_URL = "https://eve-static-data-export.s3-eu-west-1.amazonaws.com/tranquility/sde.zip"
ZIP_PATH = "sde.zip"
EXTRACT_PATH = "sde"
BLUEPRINT_OUT = "blueprints"
TYPENAME_OUT = "typeNames"
REPO_DIR = "."

print("📥 Downloading latest SDE...")
urlretrieve(SDE_URL, ZIP_PATH)

print("📦 Extracting SDE zip...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_PATH)

with open(f"{EXTRACT_PATH}/fsd/blueprints.yaml", "r", encoding="utf-8") as f:
    blueprints_data = yaml.safe_load(f)

with open(f"{EXTRACT_PATH}/fsd/types.yaml", "r", encoding="utf-8") as f:
    types_data = yaml.safe_load(f)

shutil.rmtree(BLUEPRINT_OUT, ignore_errors=True)
shutil.rmtree(TYPENAME_OUT, ignore_errors=True)
os.makedirs(BLUEPRINT_OUT, exist_ok=True)
os.makedirs(TYPENAME_OUT, exist_ok=True)

print("🧩 Splitting blueprints...")
count = 0
for bp_id, bp_data in blueprints_data.items():
    with open(f"{BLUEPRINT_OUT}/{bp_id}.json", "w", encoding="utf-8") as f:
        json.dump(bp_data, f, indent=2)
    count += 1
print(f"✅ Exported {count} blueprints to /{BLUEPRINT_OUT}")

print("🧩 Splitting typeNames...")
count = 0
for type_id, type_data in types_data.items():
    output = {
        "name": type_data.get("name", {}),
        "volume": type_data.get("volume", None)
    }
    with open(f"{TYPENAME_OUT}/{type_id}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    count += 1
print(f"✅ Exported {count} typeNames to /{TYPENAME_OUT}")

print("🚀 Committing changes to GitHub...")
repo = Repo(REPO_DIR)
repo.git.add(A=True)
repo.index.commit("🔄 Auto-update: latest SDE parsed and pushed")
repo.remote(name="origin").push()

print("🎉 Done! All data updated and pushed.")
