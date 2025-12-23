# YouTube 嵌入码保留功能

## 功能说明

这个修改版的 html2text 套件增加了自动识别和保留 YouTube 嵌入码的功能。当 HTML 内容中包含 YouTube iframe 时，转换后的 Markdown 会以 HTML 区块的形式保留这些嵌入码。

## 修改内容

### 1. 新增配置选项 (`config.py`)

```python
# Preserve YouTube iframe embeds as HTML in markdown
PRESERVE_YOUTUBE_EMBEDS = True
```

### 2. HTML2Text 类新增属性

- `preserve_youtube_embeds`: 控制是否保留 YouTube iframe（默认：True）
- `youtube_iframe_attrs`: 内部状态变量，用于跟踪当前处理的 YouTube iframe

### 3. 核心修改

- **`__init__.py`**: 在 `handle_tag` 方法中添加了 iframe 标签的处理逻辑
  - 识别 YouTube 嵌入码（通过检查 src 属性是否包含 `youtube.com` 或 `youtu.be`）
  - 将 YouTube iframe 以完整的 HTML 标签形式输出
  - 非 YouTube iframe 保持原来的行为（被忽略）

- **`utils.py`**: 修改 `skipwrap` 函数
  - 添加对 iframe 标签的检测，防止其被自动换行
  - 确保 iframe 标签在一行上输出

## 使用方法

### 基本使用

```python
import html2text

html = '''
<p>观看这个视频：</p>
<iframe width="560" height="315"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ"
        frameborder="0" allowfullscreen></iframe>
'''

h = html2text.HTML2Text()
markdown = h.handle(html)
print(markdown)
```

输出：
```markdown
观看这个视频：

<iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
```

### 关闭此功能

如果你想恢复原来的行为（忽略所有 iframe），可以设置：

```python
h = html2text.HTML2Text()
h.preserve_youtube_embeds = False
markdown = h.handle(html)
```

### 从网页 URL 转换

```python
import html2text
import urllib.request

url = 'https://example.com/page-with-youtube.html'
with urllib.request.urlopen(url) as response:
    html = response.read().decode('utf-8')

h = html2text.HTML2Text()
markdown = h.handle(html)
```

## 支持的 YouTube URL 格式

该功能会识别以下格式的 YouTube 嵌入码：

- `https://www.youtube.com/embed/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `http://` 版本（会自动升级到 https）

## 行为说明

1. **YouTube iframe**: 完整保留为 HTML 标签
2. **非 YouTube iframe**: 按原来的行为处理（被忽略）
3. **输出格式**: 每个 iframe 标签在一行上，便于阅读和编辑
4. **Markdown 兼容**: 保留的 HTML 区块完全兼容 Markdown 规范

## 测试示例

查看 `example_youtube_preservation.py` 文件获取更多使用示例。

运行示例：
```bash
python3 example_youtube_preservation.py
```

## 兼容性

- 不影响其他 HTML 转 Markdown 的功能
- 向后兼容：可以通过设置 `preserve_youtube_embeds=False` 恢复原来的行为
- 支持所有现有的 html2text 配置选项
