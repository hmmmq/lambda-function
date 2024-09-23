import json
import pandas as pd
import subprocess
import os
from tqdm import tqdm

# 获取当前目录下 image 文件夹中的所有 .tiff 文件名
image_folder = "images"
file_list = [f for f in os.listdir(image_folder) if f.endswith('.tiff')]
print(file_list)

# 初始化一个空列表来存储所有的结果
results = []

# 遍历文件列表，发送请求并收集结果
for file_name in tqdm(file_list, desc="Processing files"):
    print(f"\nProcessing {file_name}...")
    file_path = os.path.join(image_folder, file_name)
    print(f"File path {file_path}")
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", 
            "https://hybb2dhals4gioq2q7xecpdhte0hesrl.lambda-url.us-east-1.on.aws/", 
            "-H", "Content-Type: image/tiff", 
            "--data-binary", f"@{file_path}"
        ],
        capture_output=True,
        text=True
    )
     # 解析 JSON 字符串
    data = json.loads(result.stdout)
     # 添加新的属性 image_name
    data["image_name"] = file_name
    # 将结果添加到列表中
    results.append(data)
    print(f"\nComplete process {file_name}, result:\n {data}\n ")

# 将所有结果转换为 JSON 字符串
json_str = json.dumps(results)

# 解析 JSON 字符串
data = json.loads(json_str)

# 检查 data 的类型
if isinstance(data, dict):
    # 如果是字典，转换为 DataFrame
    df = pd.DataFrame([data])
elif isinstance(data, list):
    # 如果是列表，转换为 DataFrame
    df = pd.DataFrame(data)
else:
    raise ValueError("JSON 数据格式不正确")

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 将 DataFrame 保存为 Excel 文件
df.to_excel('output.xlsx', index=False)