# My AI Mini Tools (我的AI 小工具集)

这里存放我利用AI辅助编写的各种实用小脚本和自动化工具。

## 仓库目标
收集日常工作中遇到的痛点，并利用 AI（如 Gemini, ChatGPT）快速生成的解决方案。

## 工具列表 (Tools List)

| 工具名称 | 语言 | 简介 | 路径 |
| :--- | :--- | :--- | :--- |
| GIF 去白底工具 | Python | 自动去除 GIF 动图的白色背景，修复微信不透明问题 | `gif_tool/` |

## 详细使用指南

### 1. GIF 去白底工具 (GIF Background Remover)
* **位置**: `gif_tool/remove_gif_bg.py`
* **功能**:
    * 自动去除 GIF 动图的白色背景。
    * 修复了微信发送不透明的问题（兼容性优化）。
    * 解决动图重影和半透明 Bug（全帧重建模式）。

**如何使用**:
1.  确保安装了依赖: `pip install pillow`
2.  将你的 GIF 文件重命名为 `input.gif` (或者直接把脚本和 GIF 放在同一文件夹)。
3.  运行脚本:
    ```bash
    cd gif_tool
    python remove_gif_bg.py
    ```
4.  输出文件名为 `final_原文件名.gif`。

## 环境准备
建议为这些脚本创建一个统一的 Python 虚拟环境，以免依赖冲突。

```bash
# 创建虚拟环境
python -m venv venv

# 激活环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装常用依赖
pip install pillow requests pandas
