# 项目文件清单

## 📁 核心文件（必需）

### Python脚本
- ✅ `bilibili_extractor_env.py` - **推荐使用**，从环境变量读取Cookie
- ✅ `bilibili_extractor_with_cookie.py` - 直接在代码中设置Cookie
- ✅ `test_cookie.py` - 测试Cookie是否有效

### 配置文件
- ✅ `.env.example` - Cookie配置模板（复制为.env使用）
- ✅ `.env` - 实际配置文件（需要填入Cookie）

### Shell脚本
- ✅ `run_extractor.sh` - 快速启动脚本

## 📚 文档文件

### 使用指南
- ✅ `QUICK_START.md` - **快速开始指南**（推荐先看这个）
- ✅ `BILIBILI_SUBTITLE_GUIDE.md` - 详细使用指南
- ✅ `README.md` - 项目说明
- ✅ `PROJECT_SUMMARY.md` - 项目技术总结

## 🔧 开发/测试文件（可选）

- 🔧 `test_bilibili_api.py` - API测试脚本
- 🔧 `bilibili_subtitle_extractor.py` - 使用bilibili-api库的版本
- 🔧 `bilibili_extractor_simple.py` - 无Cookie版本（仅供参考）

## 📊 输出目录

- 📁 `subtitles/` - 字幕输出目录（运行后生成）
  - 各个视频的独立字幕文件
  - `所有字幕汇总.txt`

## 🎯 使用流程

1. **第一次使用**
   - 阅读 `QUICK_START.md`
   - 复制 `.env.example` 为 `.env`
   - 运行 `python test_cookie.py` 测试
   - 运行 `./run_extractor.sh` 提取字幕

2. **遇到问题**
   - 查看 `BILIBILI_SUBTITLE_GUIDE.md`
   - 查看技术细节：`PROJECT_SUMMARY.md`

3. **开发者**
   - 查看 `PROJECT_SUMMARY.md` 了解技术实现
   - 运行测试脚本调试

## 📝 文件大小参考

```
bilibili_extractor_env.py         ~11KB  (推荐)
bilibili_extractor_with_cookie.py ~11KB  (备选)
test_cookie.py                    ~3KB   (测试工具)
run_extractor.sh                  ~1KB   (启动脚本)
QUICK_START.md                    ~1KB   (快速指南)
BILIBILI_SUBTITLE_GUIDE.md        ~4KB   (详细指南)
```

## ✨ 推荐使用顺序

1. `QUICK_START.md` - 快速了解如何使用
2. `.env.example` → `.env` - 配置Cookie
3. `test_cookie.py` - 验证配置
4. `run_extractor.sh` - 开始提取
5. `subtitles/` - 查看结果

## 🔍 文件用途说明

| 文件 | 用途 | 是否必需 |
|------|------|---------|
| bilibili_extractor_env.py | 主程序（推荐） | ✅ |
| .env | Cookie配置 | ✅ |
| run_extractor.sh | 快速启动 | ✅ 推荐 |
| test_cookie.py | 测试工具 | ✅ 推荐 |
| QUICK_START.md | 使用说明 | ✅ 推荐 |
| 其他文件 | 参考文档 | ⚪ 可选 |
