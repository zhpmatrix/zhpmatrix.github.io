#!/usr/bin/env python3
"""
测试B站Cookie是否有效
"""

import os
import sys
from dotenv import load_dotenv
import requests

def test_cookie():
    # 加载环境变量
    load_dotenv()
    cookie = os.getenv('BILIBILI_COOKIE')

    if not cookie:
        print("❌ 错误: 未找到Cookie")
        print("\n请先设置Cookie:")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 中填入你的Cookie")
        print("   或者设置环境变量: export BILIBILI_COOKIE='你的Cookie'")
        return False

    print("🔍 正在测试Cookie...")

    # 解析Cookie
    cookies = {}
    for item in cookie.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()

    # 检查关键字段
    required_fields = ['SESSDATA', 'bili_jct', 'DedeUserID']
    missing_fields = [f for f in required_fields if f not in cookies]

    if missing_fields:
        print(f"❌ Cookie缺少必要字段: {', '.join(missing_fields)}")
        print("\n完整的Cookie应该包含:")
        for field in required_fields:
            print(f"  - {field}")
        return False

    print("✅ Cookie包含所有必要字段")

    # 测试API请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://space.bilibili.com/1150472191',
        'Host': 'api.bilibili.com',
    }

    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)

    # 测试获取用户信息
    try:
        url = 'https://api.bilibili.com/x/space/arc/search'
        params = {'mid': 1150472191, 'ps': 1, 'pn': 1}

        response = session.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 0:
                count = data['data']['page']['count']
                print(f"✅ Cookie有效！成功连接到B站API")
                print(f"📊 产品老曾共有 {count} 个视频")
                print("\n你可以运行以下命令开始提取字幕:")
                print("  ./run_extractor.sh")
                print("  或")
                print("  python bilibili_extractor_env.py")
                return True
            else:
                print(f"❌ API返回错误: {data.get('message')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            if response.status_code == 412:
                print("\n可能的原因:")
                print("  - Cookie无效或已过期")
                print("  - Cookie格式不正确")
                print("  - 需要重新获取Cookie")
            return False

    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

if __name__ == "__main__":
    success = test_cookie()
    sys.exit(0 if success else 1)
