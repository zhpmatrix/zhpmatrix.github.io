#!/usr/bin/env python3
"""
B站UP主视频字幕提取器
用于提取指定UP主所有视频的字幕内容
"""

import asyncio
import json
import os
from pathlib import Path
from bilibili_api import video, user
import aiohttp


class BilibiliSubtitleExtractor:
    def __init__(self, uid, output_dir="subtitles"):
        self.uid = uid
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.video_list = []
        self.subtitle_data = {}

    async def get_user_videos(self):
        """获取用户所有视频"""
        print(f"正在获取用户 {self.uid} 的视频列表...")

        u = user.User(self.uid)

        # 获取视频列表
        try:
            # 获取所有视频
            videos = await u.get_videos()

            video_count = 0
            if 'list' in videos:
                for v in videos['list']:
                    vdata = v['videos']
                    self.video_list.append({
                        'bvid': vdata['bvid'],
                        'title': vdata['title'],
                        'description': vdata.get('description', ''),
                        'duration': vdata.get('duration', 0),
                        'ctime': vdata.get('ctime', 0)
                    })
                    video_count += 1

                print(f"找到 {video_count} 个视频")
                return self.video_list
            else:
                print("未找到视频列表")
                return []

        except Exception as e:
            print(f"获取视频列表失败: {e}")
            return []

    async def get_video_subtitle(self, bvid, v):
        """获取单个视频的字幕"""
        print(f"正在处理视频: {v['title']} (BVID: {bvid})")

        try:
            v_obj = video.Video(bvid=bvid)

            # 获取视频信息
            info = await v_obj.get_info()
            title = info.get('title', v['title'])

            # 获取字幕
            subtitle_obj = v_obj.subtitle

            try:
                subtitles = await subtitle_obj.get_subtitle_list()

                if not subtitles:
                    print(f"  视频没有字幕")
                    return None

                all_subtitle_text = []

                for sub in subtitles:
                    sub_id = sub['id']
                    sub_lang = sub.get('lan', 'unknown')

                    print(f"  找到字幕: {sub_lang} (ID: {sub_id})")

                    # 获取字幕内容
                    sub_data = await subtitle_obj.get_subtitle_content(sub_id)

                    if 'body' in sub_data:
                        lines = []
                        for item in sub_data['body']:
                            if 'content' in item:
                                lines.append(item['content'])

                        subtitle_text = '\n'.join(lines)
                        all_subtitle_text.append(subtitle_text)

                if all_subtitle_text:
                    combined_text = '\n\n'.join(all_subtitle_text)
                    self.subtitle_data[bvid] = {
                        'title': title,
                        'subtitle': combined_text
                    }

                    # 保存单个视频字幕到文件
                    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                    if not safe_title:
                        safe_title = bvid

                    subtitle_file = self.output_dir / f"{safe_title}.txt"
                    with open(subtitle_file, 'w', encoding='utf-8') as f:
                        f.write(f"视频标题: {title}\n")
                        f.write(f"BVID: {bvid}\n")
                        f.write(f"{'='*80}\n\n")
                        f.write(combined_text)

                    print(f"  字幕已保存到: {subtitle_file.name}")
                    return combined_text
                else:
                    print(f"  字幕内容为空")
                    return None

            except Exception as e:
                print(f"  获取字幕失败: {e}")
                return None

        except Exception as e:
            print(f"  处理视频失败: {e}")
            return None

    async def extract_all_subtitles(self):
        """提取所有视频的字幕"""
        videos = await self.get_user_videos()

        if not videos:
            print("没有找到视频")
            return

        print(f"\n开始提取 {len(videos)} 个视频的字幕...")

        success_count = 0
        fail_count = 0

        for i, v in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}]", end=" ")
            result = await self.get_video_subtitle(v['bvid'], v)

            if result:
                success_count += 1
            else:
                fail_count += 1

            # 添加延迟避免请求过快
            await asyncio.sleep(1)

        # 生成汇总文件
        self.save_combined_subtitles()

        print(f"\n\n提取完成!")
        print(f"成功: {success_count} 个视频")
        print(f"失败/无字幕: {fail_count} 个视频")
        print(f"字幕保存在: {self.output_dir.absolute()}")

    def save_combined_subtitles(self):
        """保存所有字幕到一个汇总文件"""
        if not self.subtitle_data:
            print("没有字幕数据可保存")
            return

        combined_file = self.output_dir / "所有字幕汇总.txt"

        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write("B站UP主视频字幕汇总\n")
            f.write(f"UID: {self.uid}\n")
            f.write(f"视频总数: {len(self.subtitle_data)}\n")
            f.write(f"{'='*80}\n\n")

            for i, (bvid, data) in enumerate(self.subtitle_data.items(), 1):
                f.write(f"\n\n{'='*80}\n")
                f.write(f"[{i}/{len(self.subtitle_data)}] {data['title']}\n")
                f.write(f"BVID: {bvid}\n")
                f.write(f"{'='*80}\n\n")
                f.write(data['subtitle'])

        print(f"\n汇总字幕已保存到: {combined_file.name}")


async def main():
    # 产品老曾的UID
    UID = 1150472191

    extractor = BilibiliSubtitleExtractor(UID)
    await extractor.extract_all_subtitles()


if __name__ == "__main__":
    asyncio.run(main())
