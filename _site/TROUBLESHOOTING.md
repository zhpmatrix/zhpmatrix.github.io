# 故障排除指南

## ❓ 常见问题及解决方案

### 问题1: 412 Precondition Failed

**症状**:
```
HTTP请求失败: 412
```

**原因**:
- 未设置Cookie
- Cookie格式不正确
- Cookie已过期

**解决方案**:
1. 确认已设置Cookie
   ```bash
   echo $BILIBILI_COOKIE  # 检查环境变量
   cat .env  # 检查配置文件
   ```

2. 重新获取Cookie
   - 在浏览器中重新登录B站
   - 按F12打开开发者工具
   - 复制完整的Cookie字符串
   - 更新.env文件

3. 验证Cookie格式
   - 必须包含 `SESSDATA`、`bili_jct`、`DedeUserID`
   - 不要包含引号
   - 格式: `key1=value1; key2=value2; ...`

### 问题2: 401/403 Unauthorized

**症状**:
```
API返回错误: 账号未登录
```

**原因**:
- Cookie已过期
- SESSDATA无效

**解决方案**:
1. 重新登录B站
2. 获取新的Cookie
3. 更新配置

### 问题3: 找不到视频

**症状**:
```
共找到 0 个视频
```

**原因**:
- UID错误
- 网络连接问题
- UP主没有发布视频

**解决方案**:
1. 确认UID是否正确（产品老曾: 1150472191）
2. 检查网络连接
3. 访问 https://space.bilibili.com/1150472191 确认视频存在

### 问题4: 字幕文件为空

**症状**:
```
视频没有字幕
```

**原因**:
- 该视频确实没有字幕
- 字幕数据格式变化

**解决方案**:
- 这是正常情况，不是所有视频都有字幕
- 脚本会自动跳过没有字幕的视频

### 问题5: Python导入错误

**症状**:
```
ModuleNotFoundError: No module named 'xxx'
```

**原因**:
- 缺少依赖包

**解决方案**:
```bash
pip install requests python-dotenv
```

### 问题6: 权限错误

**症状**:
```
Permission denied: './run_extractor.sh'
```

**原因**:
- 脚本没有执行权限

**解决方案**:
```bash
chmod +x run_extractor.sh
```

### 问题7: 编码错误

**症状**:
```
UnicodeEncodeError: 'ascii' codec can't encode...
```

**原因**:
- 系统编码问题

**解决方案**:
```bash
export PYTHONIOENCODING=utf-8
python bilibili_extractor_env.py
```

## 🔍 诊断步骤

### 1. 测试Cookie
```bash
python test_cookie.py
```

如果显示 `✅ Cookie有效！`，则Cookie配置正确。

### 2. 检查网络连接
```bash
curl -I https://api.bilibili.com
```

应该返回 `200 OK` 或类似的响应。

### 3. 查看详细错误
```bash
python bilibili_extractor_env.py
```

查看完整的错误信息和堆栈跟踪。

### 4. 检查文件权限
```bash
ls -la *.py *.sh
```

确保脚本有执行权限。

## 📞 获取帮助

如果以上方法都无法解决问题：

1. 查看详细文档
   - `QUICK_START.md` - 快速开始指南
   - `BILIBILI_SUBTITLE_GUIDE.md` - 详细使用指南
   - `PROJECT_SUMMARY.md` - 技术文档

2. 检查日志
   - 查看控制台输出的错误信息
   - 查看Python的堆栈跟踪

3. 验证环境
   - Python版本: 需要 Python 3.7+
   - 依赖包: requests, python-dotenv

## 🔧 高级调试

### 启用详细日志

编辑 `bilibili_extractor_env.py`，添加：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 手动测试API

```bash
# 测试获取视频列表
curl 'https://api.bilibili.com/x/space/arc/search?mid=1150472191&ps=1&pn=1' \
  -H 'Cookie: 你的Cookie'
```

### 检查Cookie内容

```python
# 临时脚本
import os
from dotenv import load_dotenv

load_dotenv()
cookie = os.getenv('BILIBILI_COOKIE')

# 检查必需字段
required = ['SESSDATA', 'bili_jct', 'DedeUserID']
for field in required:
    if field in cookie:
        print(f"✅ {field}: 存在")
    else:
        print(f"❌ {field}: 缺失")
```

## 📋 常用命令

```bash
# 测试Cookie
python test_cookie.py

# 运行提取器
./run_extractor.sh

# 查看结果
ls -la subtitles/

# 查看汇总文件
cat subtitles/所有字幕汇总.txt

# 检查Python版本
python --version

# 安装依赖
pip install requests python-dotenv

# 查看帮助
./example_usage.sh
```
