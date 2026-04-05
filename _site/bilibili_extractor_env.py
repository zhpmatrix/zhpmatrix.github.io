#!/usr/bin/env python3
"""
B站视频字幕提取器 - 环境变量版本

使用说明：
1. 设置环境变量 BILIBILI_COOKIE
2. 运行脚本

Linux/Mac:
export BILIBILI_COOKIE="你的Cookie"
python bilibili_extractor_env.py

Windows PowerShell:
$env:BILIBILI_COOKIE="你的Cookie"
python bilibili_extractor_env.py

或者创建 .env 文件：
BILIBILI_COOKIE=你的Cookie字符串
"""

import os
import requests
import time
from pathlib import Path
from dotenv import load_dotenv


class BilibiliExtractor:
    def __init__(self, uid, cookie=None, output_dir="subtitles"):
        self.uid = uid
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # 从环境变量或参数获取Cookie
        if cookie is None:
            # 尝试从.env文件加载
            load_dotenv()
            cookie = os.getenv('BILIBILI_COOKIE')

        if not cookie:
            raise ValueError(
                "未找到Cookie! 请设置环境变量 BILIBILI_COOKIE "
                "或在运行时提供Cookie参数。\n\n"
                "获取Cookie的方法：\n"
                "1. 在浏览器中登录B站\n"
                "2. 打开开发者工具(F12) -> Network标签\n"
                "3. 刷新页面，找到任意请求\n"
                "4. 在请求头中复制Cookie值\n"
                "5. 设置环境变量: export BILIBILI_COOKIE='你的Cookie'\n"
            )

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': f'https://space.bilibili.com/{uid}',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'api.bilibili.com',
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies = self.parse_cookie(cookie)

    def parse_cookie(self, cookie_str):
        """解析Cookie字符串"""
        cookies = {}
        if cookie_str:
            for item in cookie_str.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()
        return cookies

    def get_video_list(self, page=1, page_size=30):
        """获取用户视频列表"""
        url = 'https://api.bilibili.com/x/space/arc/search'

        params = {
            'mid': self.uid,
            'ps': page_size,
            'pn': page,
            'order': 'pubdate',
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get('code') == 0:
                    videos = []
                    vlist = data['data']['list']['vlist']

                    for v in vlist:
                        videos.append({
                            'bvid': v['bvid'],
                            'title': v['title'],
                            'description': v.get('description', ''),
                            'duration': v.get('length', ''),
                            'ctime': v.get('created', 0),
                            'play': v.get('play', 0),
                            'comment': v.get('comment', 0),
                        })

                    return videos, data['data']['page']['count']
                else:
                    print(f"  API返回错误: {data.get('message', '未知错误')}")
                    return [], 0
            else:
                print(f"  HTTP请求失败: {response.status_code}")
                return [], 0

        except Exception as e:
            print(f"  获取视频列表失败: {e}")
            return [], 0

    def get_all_videos(self):
        """获取所有视频"""
        all_videos = []
        page = 1
        page_size = 30

        print(f"正在获取用户 {self.uid} 的视频列表...")

        while True:
            print(f"正在获取第 {page} 页...")
            videos, total_count = self.get_video_list(page, page_size)

            if not videos:
                print(f"  没有更多视频")
                break

            all_videos.extend(videos)
            print(f"  找到 {len(videos)} 个视频 (总计: {len(all_videos)}/{total_count})")

            if len(all_videos) >= total_count:
                break

            page += 1
            time.sleep(0.5)

        print(f"共找到 {len(all_videos)} 个视频")
        return all_videos

    def get_video_subtitle(self, bvid):
        """获取视频字幕"""
        try:
            # 获取视频信息
            info_url = 'https://api.bilibili.com/x/web-interface/view'
            params = {'bvid': bvid}
            response = self.session.get(info_url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"  获取视频信息失败: HTTP {response.status_code}")
                return None

            data = response.json()
            if data.get('code') != 0:
                print(f"  获取视频信息失败: {data.get('message')}")
                return None

            video_data = data['data']
            title = video_data['title']
            cid = video_data['cid']

            # 获取字幕列表
            subtitle_url = 'https://api.bilibili.com/x/player/v2'
            params = {
                'bvid': bvid,
                'cid': cid,
            }

            response = self.session.get(subtitle_url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"  获取字幕信息失败: HTTP {response.status_code}")
                return None

            subtitle_data = response.json()
            if subtitle_data.get('code') != 0:
                print(f"  获取字幕信息失败: {subtitle_data.get('message')}")
                return None

            # 检查是否有字幕
            subtitle_info = subtitle_data['data'].get('subtitle')
            if not subtitle_info or not subtitle_info.get('subtitles'):
                print(f"  视频没有字幕")
                return None

            all_subtitle_text = []

            # 获取每个字幕文件
            for sub in subtitle_info['subtitles']:
                sub_url = sub['subtitle_url']
                sub_lang = sub.get('lan_doc', 'unknown')

                print(f"  找到字幕: {sub_lang}")

                # 获取字幕内容
                sub_response = self.session.get(f'https:{sub_url}', timeout=10)
                if sub_response.status_code == 200:
                    sub_content = sub_response.json()

                    if 'body' in sub_content:
                        lines = []
                        for item in sub_content['body']:
                            if 'content' in item:
                                lines.append(item['content'])

                        subtitle_text = '\n'.join(lines)
                        all_subtitle_text.append(subtitle_text)

            if all_subtitle_text:
                combined_text = '\n\n'.join(all_subtitle_text)
                return {
                    'title': title,
                    'subtitle': combined_text
                }
            else:
                return None

        except Exception as e:
            print(f"  获取字幕失败: {e}")
            return None

    def extract_all_subtitles(self):
        """提取所有视频的字幕"""
        videos = self.get_all_videos()

        if not videos:
            print("没有找到视频")
            return

        print(f"\n开始提取 {len(videos)} 个视频的字幕...")

        subtitle_data = {}
        success_count = 0
        fail_count = 0

        for i, v in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] {v['title'][:50]}...")

            result = self.get_video_subtitle(v['bvid'])

            if result:
                success_count += 1
                subtitle_data[v['bvid']] = result

                # 保存单个视频字幕
                safe_title = "".join(c for c in result['title'] if c.isalnum() or c in (' ', '-', '_', '：', '【', '】', '（', '）', '、', '，')).strip()
                if not safe_title:
                    safe_title = v['bvid']

                if len(safe_title) > 100:
                    safe_title = safe_title[:100]

                subtitle_file = self.output_dir / f"{safe_title}.txt"
                with open(subtitle_file, 'w', encoding='utf-8') as f:
                    f.write(f"视频标题: {result['title']}\n")
                    f.write(f"BVID: {v['bvid']}\n")
                    f.write(f"播放量: {v['play']}\n")
                    f.write(f"时长: {v['duration']}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(result['subtitle'])

                print(f"  字幕已保存: {subtitle_file.name}")
            else:
                fail_count += 1

            time.sleep(1)

        # 保存汇总文件
        self.save_combined_subtitles(subtitle_data)

        print(f"\n\n提取完成!")
        print(f"成功: {success_count} 个视频")
        print(f"失败/无字幕: {fail_count} 个视频")
        print(f"字幕保存在: {self.output_dir.absolute()}")

    def save_combined_subtitles(self, subtitle_data):
        """保存所有字幕到汇总文件"""
        if not subtitle_data:
            print("没有字幕数据可保存")
            return

        combined_file = self.output_dir / "所有字幕汇总.txt"

        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("B站UP主视频字幕汇总\n")
            f.write(f"UID: {self.uid}\n")
            f.write(f"视频总数: {len(subtitle_data)}\n")
            f.write(f"{'='*80}\n\n")

            for i, (bvid, data) in enumerate(subtitle_data.items(), 1):
                f.write(f"\n\n{'='*80}\n")
                f.write(f"[{i}/{len(subtitle_data)}] {data['title']}\n")
                f.write(f"BVID: {bvid}\n")
                f.write(f"{'='*80}\n\n")
                f.write(data['subtitle'])

        print(f"\n汇总字幕已保存到: {combined_file.name}")


def main():
    # 产品老曾的UID
    UID = 1150472191

    try:
        extractor = BilibiliExtractor(UID)
        extractor.extract_all_subtitles()
    except ValueError as e:
        print(f"错误: {e}")
        return 1
    except Exception as e:
        print(f"运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
