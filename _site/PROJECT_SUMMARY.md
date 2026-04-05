# B站视频字幕提取工具 - 项目总结

## 📌 项目目标

从B站UP主"产品老曾"的个人空间（https://space.bilibili.com/1150472191）提取所有视频的字幕内容，并保存为文本文件。

## 🚧 技术挑战

### 1. B站反爬虫保护
- **问题**: 直接访问API会遇到 `412 Precondition Failed` 错误
- **原因**: B站的安全风控策略阻止了未经授权的API请求
- **解决**: 需要使用登录后的Cookie才能正常访问

### 2. Cookie获取
- **问题**: 需要从浏览器获取有效的Cookie
- **解决**: 提供了详细的Cookie获取指南

### 3. API接口变化
- **问题**: B站API可能随时变化
- **解决**: 使用稳定的API端点和正确的请求格式

## 📦 项目文件

### 核心脚本

1. **bilibili_extractor_env.py** (推荐)
   - 从环境变量或.env文件读取Cookie
   - 支持自动配置
   - 最安全的方式

2. **bilibili_extractor_with_cookie.py**
   - 直接在代码中设置Cookie
   - 适合快速测试

3. **bilibili_extractor_simple.py**
   - 无Cookie版本
   - 仅供参考（会被拦截）

4. **test_bilibili_api.py**
   - API测试脚本
   - 用于调试

5. **test_cookie.py**
   - Cookie验证脚本
   - 测试Cookie是否有效

### 配置文件

6. **.env.example**
   - Cookie配置模板
   - 使用说明

7. **.env**
   - 实际配置文件
   - 包含用户的Cookie

### 辅助文件

8. **run_extractor.sh**
   - 快速启动脚本
   - 自动检查配置

9. **BILIBILI_SUBTITLE_GUIDE.md**
   - 详细使用指南
   - 故障排除

10. **README.md**
    - 项目说明
    - 快速开始指南

## 🔧 使用方法

### 方法1：快速启动（推荐）

```bash
# 1. 复制配置文件
cp .env.example .env

# 2. 编辑.env，填入Cookie
nano .env

# 3. 测试Cookie
python test_cookie.py

# 4. 运行提取器
./run_extractor.sh
```

### 方法2：使用环境变量

```bash
export BILIBILI_COOKIE="你的Cookie"
python bilibili_extractor_env.py
```

## 📊 输出结果

### 目录结构
```
subtitles/
├── 视频1标题.txt
├── 视频2标题.txt
├── 视频3标题.txt
├── ...
└── 所有字幕汇总.txt
```

### 文件内容

每个字幕文件包含：
- 视频标题
- BVID
- 播放量
- 时长
- 完整字幕内容

## 🔑 核心技术

### API端点

1. **获取视频列表**
   ```
   GET https://api.bilibili.com/x/space/arc/search
   参数: mid, ps, pn, order
   ```

2. **获取视频信息**
   ```
   GET https://api.bilibili.com/x/web-interface/view
   参数: bvid
   ```

3. **获取字幕列表**
   ```
   GET https://api.bilibili.com/x/player/v2
   参数: bvid, cid
   ```

4. **获取字幕内容**
   ```
   GET https://aisubtitle.bilibili.com/...
   ```

### 请求头设置

```python
headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Referer': 'https://space.bilibili.com/{uid}',
    'Accept': 'application/json, text/plain, */*',
    'Host': 'api.bilibili.com',
}
```

### Cookie要求

必需字段：
- `SESSDATA` - 身份验证（最重要）
- `bili_jct` - CSRF令牌
- `DedeUserID` - 用户ID

## ⚠️ 注意事项

1. **Cookie有效期**: 约30天，过期需重新获取
2. **请求频率**: 内置延迟，避免被限制
3. **字幕可用性**: 不是所有视频都有字幕
4. **隐私保护**: Cookie包含敏感信息，请勿泄露

## 🐛 故障排除

### 412错误
- 原因: Cookie无效或未设置
- 解决: 重新获取Cookie

### 401/403错误
- 原因: Cookie过期
- 解决: 重新登录获取新Cookie

### 无视频
- 原因: UID错误或网络问题
- 解决: 检查UID和网络连接

## 📚 参考资源

- [B站API文档集合](https://github.com/SocialSisterYi/bilibili-API-collect)
- [bilibili-api-python库](https://pypi.org/project/bilibili-api-python/)
- [B站反爬虫讨论](https://github.com/DIYgod/RSSHub/issues/20406)
- [获取B站Cookie指南](https://gist.github.com/monSteRhhe/a921a7ea8f2b88088e5eee2de73ecd03)

## 📝 后续改进

1. 支持多线程加速
2. 添加断点续传功能
3. 支持导出为多种格式（Markdown、JSON等）
4. 添加进度条显示
5. 支持批量处理多个UP主

## 🎯 总结

本项目成功实现了从B站提取视频字幕的功能，通过使用Cookie绕过了反爬虫限制。提供了多种使用方式，详细的文档和测试工具，确保用户能够顺利使用。

## 📄 许可证

仅供学习和个人使用，请遵守B站服务条款。
