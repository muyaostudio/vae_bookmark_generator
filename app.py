#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: app.py
# Author: muyaostudio
# Date: 2025-05-31

import gradio as gr
import json
import os
from PIL import Image, ImageDraw, ImageFont

# 加载中文字体
font_path = "assets/AlibabaPuHuiTi-3-85-Bold.ttf"
font_name = ImageFont.truetype(font_path, 65*2)
font_lrc = ImageFont.truetype(font_path, 43*2)

# 加载数据
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载数据失败: {e}")
        return {"albums": []}

# 更新歌曲和歌词下拉
def update_songs_and_lyrics(album, data):
    for a in data["albums"]:
        if a["name"] == album:
            songs = a["songs"]
            song_names = [s["name"] for s in songs]
            default_song = song_names[0] if song_names else ""
            default_lyrics_choices = songs[0]["lyrics"] if songs[0]["lyrics"] else []
            default_lyrics_value = default_lyrics_choices[0] if default_lyrics_choices else ""
            return (
                gr.update(choices=song_names, value=default_song),
                gr.update(choices=default_lyrics_choices, value=default_lyrics_value)
            )
    return (
        gr.update(choices=[], value=""),
        gr.update(choices=[], value="")
    )

def update_lyrics(album, song, data):
    for a in data["albums"]:
        if a["name"] == album:
            for s in a["songs"]:
                if s["name"] == song:
                    lyrics_choices = s.get("lyrics", [])
                    return gr.update(choices=lyrics_choices, value=lyrics_choices[0] if lyrics_choices else "")
    return gr.update(choices=[], value="")

# 生成书签图像（仅封面图、歌名、歌词）
def generate_bookmark(album, song, lyric, data):
    try:
        cover_path = None
        for a in data["albums"]:
            if a["name"] == album:
                cover_path = a.get("cover")
                break

        if cover_path and os.path.exists(cover_path):
            img = Image.open(cover_path).convert("RGB")
        else:
            img = Image.new('RGB', (1200*2, 500*2), color=(0, 0, 0))
        img = img.resize((1200*2, 500*2))

        draw = ImageDraw.Draw(img)

        draw.text((460*2, 80*2), f"{song} - 许嵩", font=font_name, fill=(51, 51, 51))
        draw.text((460*2, 180*2), lyric if len(lyric.replace(" ",""))<=16 else f"{lyric[:15]}...", font=font_lrc, fill=(51, 51, 51))

        # 保存 PNG 文件到临时目录
        output_path = f"output/bookmark.png"
        os.makedirs("output", exist_ok=True)
        img.save(output_path, format="PNG")
        
        return img
    except Exception as e:
        print(f"生成图片失败: {e}")
        return None

# 构建 Gradio 界面
def create_app():
    data = load_data("data/songs.json")

    default_album = data["albums"][0]["name"] if data["albums"] else ""
    default_songs = data["albums"][0]["songs"] if data["albums"] else []
    default_song = default_songs[0]["name"] if default_songs else ""
    default_lyrics_list = default_songs[0]["lyrics"] if default_songs and "lyrics" in default_songs[0] else []
    default_lyric = default_lyrics_list[0] if default_lyrics_list else ""

    with gr.Blocks(title="播放器样式书签生成器", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 许嵩播放器样式书签生成器")
        gr.Markdown("选择专辑、歌曲、歌词，生成你的专属封面书签")

        with gr.Row():
            with gr.Column(scale=1):
                album = gr.Dropdown(
                    label="选择专辑",
                    choices=[a["name"] for a in data["albums"]],
                    value=default_album
                )

                song = gr.Dropdown(
                    label="选择歌曲",
                    choices=[s["name"] for s in default_songs],
                    value=default_song
                )

                lyrics = gr.Dropdown(
                    label="选择歌词",
                    choices=default_lyrics_list,
                    value=default_lyric
                )

                generate_btn = gr.Button("生成书签", variant="primary")

                album.change(
                    fn=update_songs_and_lyrics,
                    inputs=[album, gr.State(data)],
                    outputs=[song, lyrics]
                )

                song.change(
                    fn=update_lyrics,
                    inputs=[album, song, gr.State(data)],
                    outputs=lyrics
                )

            with gr.Column(scale=1):
                output_image = gr.Image(label="生成的书签", type="pil")

        generate_btn.click(
            fn=lambda a, s, l: generate_bookmark(a, s, l, data),
            inputs=[album, song, lyrics],
            outputs=output_image
        )

        gr.Markdown("""
        ### 使用说明
        1. 选择专辑、歌曲、歌词，点击“生成书签”即可生成
        3. 书签像素为 2400x1200（尺寸为 12:5）
        4. 数据来自 `data/songs.json`，可自行增删
        """, height=200)

    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, show_api=False)
