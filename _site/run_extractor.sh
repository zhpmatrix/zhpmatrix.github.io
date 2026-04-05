#!/bin/bash
# B站字幕提取工具 - 快速启动脚本

echo "======================================"
echo "  B站视频字幕提取工具"
echo "  UP主: 产品老曾 (UID: 1150472191)"
echo "======================================"
echo ""

# 检查是否设置了Cookie
if [ -z "$BILIBILI_COOKIE" ]; then
    # 检查是否有.env文件
    if [ -f ".env" ]; then
        echo "从.env文件加载配置..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "错误: 未找到B站Cookie!"
        echo ""
        echo "请先设置Cookie:"
        echo "1. 复制 .env.example 为 .env"
        echo "2. 在 .env 中填入你的Cookie"
        echo "   或者设置环境变量: export BILIBILI_COOKIE='你的Cookie'"
        echo ""
        echo "获取Cookie的方法:"
        echo "1. 在浏览器中登录B站"
        echo "2. 按F12打开开发者工具 -> Network标签"
        echo "3. 刷新页面，找到任意请求"
        echo "4. 在请求头中复制Cookie值"
        echo ""
        exit 1
    fi
fi

# 运行提取器
echo "开始提取字幕..."
echo ""

python bilibili_extractor_env.py

echo ""
echo "完成!"
