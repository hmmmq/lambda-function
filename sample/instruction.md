## 以下是运行 `json_transfer_excel.py` 文件的说明文档，包括环境安装和 `image` 文件夹配置。

# 运行说明文档

## 环境安装

### 1. 安装 Python

确保你的系统已经安装了 Python 3.8 或更高版本。如果没有安装，请访问 Python 官方网站(https://www.python.org/downloads/)下载并安装。

#### 1.2 检查 python 版本

在终端中运行以下命令：

```bash
python --version
```

或者

```bash
python3 --version
```

### 2. 创建虚拟环境

建议使用虚拟环境来管理依赖项。你可以使用 `venv` 模块来创建虚拟环境。

```bash
python -m venv myenv
```

激活虚拟环境：

- 对于 macOS 和 Linux：

  ```bash
  source myenv/bin/activate
  ```

- 对于 Windows：

  ```bash
  myenv\Scripts\activate
  ```

#### 2.1 检查当前所处的虚拟环境

```bash
which python
```

这将显示当前使用的 Python 可执行文件的路径。如果你处于虚拟环境中，路径将指向虚拟环境中的 Python 可执行文件。

### 3. 安装依赖项

在虚拟环境中，使用 `pip` 安装所需的依赖项。首先，确保你在 `json_transfer_excel.py`文件所在的目录中，然后运行以下命令：

```bash
pip install pandas
```

检查是否安装了 pandas

```bash
pip show pandas
```

如果 Pandas 已安装，你将看到有关 Pandas 包的信息。

## 配置 `image`文件夹

### 1. 创建 `image` 文件夹(已经创建了,可跳过)

在 `json_transfer_excel.py`的文件夹。

```bash
mkdir images
```

### 2. 添加 `.tiff` 文件(如果你要添加文件)

1. 将你要处理的所有 `.tiff` 文件放入 `images`文件夹中。确保这些文件的扩展名为 `.tiff`。
2. 为了测试,你也可以将文件代码中的

```bash
image_folder = "images"
```

改为`demo_images`,这个文件夹里面只有一个.tiff 文件

```bash
image_folder = "demo_images"
```

## 运行脚本

确保你已经激活了虚拟环境，并且 `images`文件夹中包含了 `.tiff` 文件。然后运行 `json_transfer_excel.py`脚本：

```bash
python json_transfer_excel.py
```

## 脚本功能

1. 脚本会扫描 `images`文件夹中的所有 `.tiff` 文件。
2. 对每个 `.tiff` 文件，脚本会发送一个 HTTP POST 请求到指定的 URL。
3. 服务器返回的 JSON 响应会被解析，并添加一个新的属性 `image_name`，其值为对应的 `.tiff` 文件名。
4. 所有的结果会被集成到一个 Pandas DataFrame 中，并保存为 `output.xlsx`文件。

## 输出

脚本运行完成后，会在当前目录下生成一个名为 `output.xlsx`的 Excel 文件，其中包含所有处理过的 `.tiff` 文件的结果。

---
