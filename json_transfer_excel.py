import json
import pandas as pd
import subprocess

# 执行 curl 命令并捕获输出
result = subprocess.run(
    [
        "curl", "-s", "-X", "POST", 
        "https://hybb2dhals4gioq2q7xecpdhte0hesrl.lambda-url.us-east-1.on.aws/", 
        "-H", "Content-Type: image/tiff", 
        "--data-binary", "@aniso_dir_030_02.tiff"
    ],
    capture_output=True,
    text=True
)


# 示例 JSON 字符串
json_str = result.stdout

# 解析 JSON 字符串
data = json.loads(json_str)

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 将 DataFrame 保存为 Excel 文件
df.to_excel('output.xlsx', index=False)