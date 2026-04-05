#!/usr/bin/env python3
"""
测试B站API响应格式
"""

import asyncio
import json
from bilibili_api import user


async def test_api():
    UID = 1150472191

    u = user.User(UID)

    print("测试获取用户信息...")
    try:
        user_info = await u.get_user_info()
        print("用户信息:")
        print(json.dumps(user_info, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*80 + "\n")

    print("测试获取视频列表...")
    try:
        videos = await u.get_videos()
        print("视频列表数据类型:", type(videos))
        print("视频列表键:", videos.keys() if isinstance(videos, dict) else "不是字典")

        # 保存完整响应到文件
        with open('bilibili_api_response.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)

        print("完整响应已保存到 bilibili_api_response.json")

        print("\n视频列表内容预览:")
        print(json.dumps(videos, ensure_ascii=False, indent=2)[:2000])

    except Exception as e:
        print(f"获取视频列表失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_api())
