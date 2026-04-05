# B站视频字幕提取工具使用指南

这个工具用于从B站UP主"产品老曾"的个人空间提取所有视频的字幕内容。

## 问题说明

由于B站的反爬虫保护机制，直接访问API会遇到412错误。需要使用登录后的Cookie才能正常访问。

## 获取Cookie的详细步骤

### 方法一：使用浏览器开发者工具（推荐）

1. **打开浏览器并登录B站**
   - 访问 https://www.bilibili.com
   - 登录你的账号

2. **打开开发者工具**
   - Windows/Linux: 按 `F12` 或 `Ctrl+Shift+I`
   - Mac: 按 `Cmd+Option+I`

3. **切换到Network标签**
   - 在开发者工具中找到并点击"Network"（网络）标签

4. **刷新页面**
   - 按 `F5` 或点击刷新按钮
   - 你会看到很多网络请求

5. **找到请求并复制Cookie**
   - 点击任意一个请求（建议选择 `bilibili.com` 域名的请求）
   - 在右侧面板中找到"Headers"（标头）部分
   - 向下滚动找到"Request Headers"（请求标头）
   - 找到 `Cookie:` 这一行
   - 复制整个Cookie字符串（很长的一段文本）

### 方法二：从Application标签获取

1. 打开开发者工具（F12）
2. 切换到"Application"（应用）或"Storage"（存储）标签
3. 左侧找到"Cookies" → "https://www.bilibili.com"
4. 复制以下三个关键字段的值：
   - `SESSDATA`
   - `bili_jct`
   - `DedeUserID`

## 使用方法

### 方式1：使用带Cookie的版本（推荐）

1. 打开文件 `bilibili_extractor_with_cookie.py`

2. 找到以下部分：
   ```python
   COOKIE = """
   在这里粘贴你的Cookie
   示例格式: SESSDATA=xxxxx; bili_jct=xxxxx; DedeUserID=xxxxx; ...
   """.strip()
   ```

3. 将你复制的Cookie粘贴进去，替换原有内容

4. 运行脚本：
   ```bash
   python bilibili_extractor_with_cookie.py
   ```

### 方式2：手动设置环境变量

```bash
export BILIBILI_COOKIE="你的Cookie字符串"
python bilibili_extractor_with_cookie.py
```

## 输出结果

脚本会在当前目录下创建一个 `subtitles` 文件夹，包含：

1. **单个视频字幕文件**
   - 每个有字幕的视频都会有一个独立的 `.txt` 文件
   - 文件名格式: `视频标题.txt`
   - 包含视频信息和完整的字幕内容

2. **汇总文件**
   - 文件名: `所有字幕汇总.txt`
   - 包含所有视频的字幕内容
   - 按视频顺序排列

## 注意事项

1. **Cookie有效期**
   - Cookie会过期，如果遇到401或403错误，需要重新获取Cookie
   - 通常Cookie有效期为30天左右

2. **请求频率**
   - 脚本内置了延迟，避免请求过快被限制
   - 请勿手动修改延迟时间

3. **字幕可用性**
   - 不是所有视频都有字幕
   - 脚本会自动跳过没有字幕的视频

4. **文件名长度**
   - 部分视频标题很长，文件名会被自动截断
   - 但内容不会受影响

## 故障排除

### 遇到412错误
- 原因：Cookie无效或未设置
- 解决：重新获取Cookie并更新

### 遇到401/403错误
- 原因：Cookie已过期
- 解决：重新登录B站并获取新的Cookie

### 找不到视频
- 原因：UID错误或UP主没有发布视频
- 解决：确认UID是否正确

## 技术说明

工具使用的B站API端点：

1. **获取视频列表**: `https://api.bilibili.com/x/space/arc/search`
2. **获取视频信息**: `https://api.bilibili.com/x/web-interface/view`
3. **获取字幕列表**: `https://api.bilibili.com/x/player/v2`
4. **获取字幕内容**: `https://aisubtitle.bilibili.com/...`

## 参考资料

- [B站API文档集合](https://github.com/SocialSisterYi/bilibili-API-collect)
- [B站反爬虫解决方案讨论](https://github.com/DIYgod/RSSHub/issues/20406)

---

如果你在使用过程中遇到问题，请检查：
1. Cookie是否正确设置
2. 网络连接是否正常
3. Python环境和依赖是否完整
