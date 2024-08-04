# Dmhylib

Dmhylib 是一个用于搜索动漫花园的 Python 库。它提供了一个 `DmhySearch` 类，可以用来搜索、选择和保存搜索结果。

## 安装

可以通过 pip 安装:

```
pip install dmhylib
```

## 使用方法

### 导入

```python
from dmhylib import DmhySearch
```

### 创建搜索对象

```python
search = DmhySearch(parser='lxml', verify=True)
```

- `parser`: BeautifulSoup 解析器，默认为 'lxml'
- `verify`: 是否验证 SSL 证书，默认为 True

### 执行搜索

```python
searcher.search(keyword="关键词", sort_id=0, team_id=0, order='date-desc', proxies=None, system_proxy=False)
```

- `keyword`: 搜索关键词
- `sort_id`: 排序 ID，默认为 0。可用的排序 ID 有: 0, 2, 31, 3, 41, 42, 4, 43, 44, 15, 6, 7, 9, 17, 18, 19, 20, 21, 12, 1
- `team_id`: 团队 ID，默认为 0
- `order`: 排序顺序，默认为 'date-desc'
- `proxies`: 代理设置，默认为 None
- `system_proxy`: 是否使用系统代理，默认为 False

### 选择搜索结果

```python
searcher.select(num)
```

- `num`: 要选择的搜索结果的索引

### 格式化文件大小

```python
searcher.size_format()
```

将选中项的文件大小格式化为 MB。

### 保存为 CSV

```python
searcher.save_csv(filename)
```

- `filename`: 要保存的 CSV 路径

将选中的搜索结果保存到 CSV 文件中。

## 属性

搜索后，可以通过以下属性访问结果:

- `search.sum`: 搜索结果总数
- `search.titles`: 标题列表
- `search.pikpak_urls`: PikPak 链接列表
- `search.sizes`: 文件大小列表
- `search.magnets`: 磁力链接列表

选择某个结果后，可以通过以下属性访问选中项:

- `search.title`: 选中项的标题
- `search.pikpak_url`: 选中项的 PikPak 链接
- `search.size`: 选中项的文件大小
- `search.magnet`: 选中项的磁力链接

## 示例

```python
from dmhylib import DmhySearch

# 创建搜索对象
search = DmhySearch()

# 执行搜索
search.search(keyword="我推的孩子")

# 选择第一个结果
search.select(0)

# 格式化文件大小
search.size_format()

# 保存到 CSV 文件
search.save_csv("results.csv")
```

## 注意事项

- 在使用 `select()`, `size_format()`, 或 `save_csv()` 方法之前，必须先调用 `search()` 方法。
- `size_format()` 和 `save_csv()` 方法必须在 `select()` 方法之后调用。

## 依赖

本库依赖于以下 Python 包:

- BeautifulSoup4
- lxml
- requests
- rich

## 命令行界面（CLI）使用

Dmhylib 附赠了一个命令行界面，可以直接在终端中使用。

### 基本用法

```
dmhysearch search -k <关键词> [选项]
```

### 参数说明

- `-k`, `--keyword`: (必需) 搜索关键词
- `-s`, `--sort-id`: (可选) 搜索分类ID
- `-t`, `--team-id`: (可选) 发布团队ID
- `-o`, `--order`: (可选) 排序方式

### 示例

1. 基本搜索：

```
dmhysearch search -k "我推的孩子"
```

2. 使用特定分类ID搜索：

```
dmhysearch search -k "我推的孩子" -s 31
```

3. 指定团队ID和排序方式：

```
dmhysearch search -k "我推的孩子" -t 619 -o "date-desc"
# "619"是桜都字幕组
```

### 使用流程

1. 运行搜索命令后，程序会显示搜索结果列表，包括序号、标题和文件大小。

2. 用户可以输入想要选择的项目的序号。

3. 如果选择了有效的序号，程序会显示所选项目的标题和磁力链接。

4. 输入 0 可以退出选择过程。

### 注意事项

- 如果不确定可用的参数，可以参考 dmhy.org 的查询字符串。

### 获取帮助

要查看所有可用的命令和选项，可以运行：

```
dmhysearch --help
```

或者查看特定命令的帮助：

```
dmhysearch search --help
```

## 许可证

本项目使用 GPL-3.0 许可证