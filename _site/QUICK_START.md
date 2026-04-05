# 快速开始指南

## 🎯 三步提取字幕

### 第1步：获取Cookie

1. 打开浏览器，访问 https://www.bilibili.com 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Network` 标签
4. 刷新页面（`F5`）
5. 点击任意请求，找到 `Request Headers` 中的 `Cookie`
6. 复制整个Cookie字符串（很长，包含很多字段）

### 第2步：配置工具

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置文件
nano .env  # 或使用其他编辑器

# 将复制的Cookie粘贴到 BILIBILI_COOKIE= 后面
# 保存并退出
```

### 第3步：运行

```bash
# 测试Cookie是否有效
python test_cookie.py

# 如果测试通过，运行提取器
./run_extractor.sh
```

## 📊 查看结果

提取完成后，查看 `subtitles/` 目录：

```bash
ls -la subtitles/
```

你会看到：
- 每个视频的独立字幕文件
- `所有字幕汇总.txt` - 包含所有字幕

## ❓ 遇到问题？

查看详细指南：`BILIBILI_SUBTITLE_GUIDE.md`

## 🔧 其他使用方式

### 方式2：直接设置环境变量

```bash
export BILIBILI_COOKIE="你的Cookie"
python bilibili_extractor_env.py
```

### 方式3：修改代码

1. 打开 `bilibili_extractor_with_cookie.py`
2. 找到 `COOKIE = """..."""`
3. 粘贴你的Cookie
4. 运行：`python bilibili_extractor_with_cookie.py`
