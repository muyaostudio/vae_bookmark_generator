# 🎵 许嵩播放器样式书签生成器

一个基于 Gradio 的 Web 应用，用于生成带有许嵩专辑封面、歌曲名与歌词的播放器风格书签图像。该项目为非盈利/非商用的开源项目。

![效果预览](assets/preview.png)

## 🖼️ 功能说明

- 支持从本地 JSON 文件中读取专辑/歌曲/歌词信息，并支持级联选择
- 自动加载专辑封面图作为书签背景，并输出高清 PNG 书签
- 书签图片尺寸为 `2400x1000`，尺寸 12:5，适合打印或收藏


## 📂 项目结构

```
.
├── app.py                   # 主程序
├── data/
│   └── songs.json           # 音乐数据文件
├── assets/
│   └── *.ttf                # 字体文件
│   └── *.png                # 专辑封面图
├── output/
│   └── 531天津-8套.pdf       # 天津站发放成品
│   └── bookmark.png         # 生成的书签图像
└── README.md                # 项目说明文件
````


## 📦 安装依赖

确保你已安装 Python 3.7 以上版本。

```bash
pip install gradio pillow
````


## 🚀 启动项目

运行以下命令启动 Gradio Web 应用：

```bash
python app.py
```

默认会在本地打开浏览器访问 `http://127.0.0.1:7860`。

如需指定端口（如 8080），可修改 app.py 的以下内容：

```bash
app.launch(server_port=8080, show_api=False)
```


## 📝 自定义数据

你可以通过编辑 `data/songs.json` 文件添加或修改各个专辑中的歌曲及歌词。例如：

```json
{
  "albums": [
    {
      "name": "呼吸之野",
      "cover": "assets/呼吸之野.png",
      "songs": [
        {
          "name": "乌鸦",
          "lyrics": [
            "就当作是我不吉利 不能拥有美好幸运",
            "当我又飞到这里 俯瞰着模糊山顶"
          ]
        }
      ]
    }
  ]
}
```


## 🧩 注意事项

* 所有封面图需放置在 `assets/` 目录下，并确保路径正确。
* 输出图像默认保存在 `output/bookmark.png`，格式为 PNG。


## 🙋‍♂️ 联系作者

如有问题或建议欢迎提交 Issue 或联系作者（公众号：木尧工作室）。

音乐纯粹，爱V绝对！
