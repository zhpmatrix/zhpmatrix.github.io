# My blog

You can communicate with me as following:

- 微信公众号：《KBQA沉思录》，有惊喜～

---

## B站UP主"产品老曾"视频字幕提取工具

这个工具可以自动从B站UP主"产品老曾"的个人空间提取所有视频的字幕内容。

### 🚀 快速开始

1. **获取Cookie**
   - 在浏览器中登录B站 (https://www.bilibili.com)
   - 按 `F12` 打开开发者工具，切换到 `Network` 标签
   - 刷新页面，复制 `Cookie` 值

2. **配置并运行**
   ```bash
   # 复制配置文件模板
   cp .env.example .env

   # 编辑.env文件，粘贴Cookie
   # 然后运行
   ./run_extractor.sh
   ```

### 📁 文件说明

- `bilibili_extractor_env.py` - 推荐版本，从环境变量或.env文件读取Cookie
- `bilibili_extractor_with_cookie.py` - 直接在代码中设置Cookie的版本
- `run_extractor.sh` - 快速启动脚本
- `BILIBILI_SUBTITLE_GUIDE.md` - 详细使用指南

### 📊 输出结果

运行成功后，会在 `subtitles/` 目录下生成：
- 单个视频字幕文件（`视频标题.txt`）
- 汇总文件（`所有字幕汇总.txt`）

详细说明请查看 `BILIBILI_SUBTITLE_GUIDE.md`。
