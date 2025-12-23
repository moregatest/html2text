#!/usr/bin/env python3
"""
示例：如何使用 html2text 保留 YouTube 嵌入码

这个脚本演示了如何使用修改后的 html2text 套件
将 HTML 中的 YouTube 嵌入码保留为 markdown HTML 区块。
"""

import html2text

# 示例 HTML 内容包含 YouTube 嵌入码
html_content = """
<html>
<body>
    <h1>我的视频教程</h1>

    <p>这是第一个视频：</p>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            frameborder="0" allowfullscreen></iframe>

    <p>这是第二个视频：</p>
    <iframe width="560" height="315" src="https://www.youtube.com/embed/oHg5SJYRHA0"
            frameborder="0" allowfullscreen></iframe>

    <p>这是一个普通的链接：<a href="https://example.com">示例网站</a></p>

    <p>这是一个非 YouTube 的 iframe（会被忽略）：</p>
    <iframe src="https://example.com/embed"></iframe>
</body>
</html>
"""

# 方法 1：使用默认设置（会保留 YouTube iframe）
print("=== 方法 1：默认设置（保留 YouTube iframe）===")
h = html2text.HTML2Text()
markdown = h.handle(html_content)
print(markdown)

# 方法 2：关闭 YouTube iframe 保留功能
print("\n=== 方法 2：关闭 YouTube iframe 保留功能 ===")
h2 = html2text.HTML2Text()
h2.preserve_youtube_embeds = False
markdown2 = h2.handle(html_content)
print(markdown2)

# 方法 3：从网页 URL 转换
print("\n=== 方法 3：从网页 URL 转换 ===")
try:
    import urllib.request

    url = 'https://www.jianpins.com/factory-page/inspection-and-packing.html'
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    h3 = html2text.HTML2Text()
    h3.body_width = 0  # 不自动换行
    result = h3.handle(html)

    # 只显示包含 YouTube iframe 的部分
    lines = result.split('\n')
    for i, line in enumerate(lines):
        if '<iframe' in line and 'youtube.com' in line:
            # 显示前后各 2 行的上下文
            start = max(0, i-2)
            end = min(len(lines), i+3)
            print('\n'.join(lines[start:end]))
            print()
            break

except Exception as e:
    print(f"无法获取网页: {e}")

print("\n=== 完成 ===")
