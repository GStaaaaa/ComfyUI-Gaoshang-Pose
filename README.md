# 高尚姿势编辑器 · Gaoshang Pose

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/GStaaaaa/ComfyUI-Gaoshang-Pose/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

在 ComfyUI 中摆好人物动作、转身和站位，再将姿势参考图接入 Qwen Image 2.1 图像编辑工作流。

支持 **1–9 个人偶独立编辑、9 张人物参考图、彩色编号选人**，适合编排多人构图与剧情站位。

![高尚姿势编辑器界面](docs/editor.png)

## 功能

- **最多 9 人**：添加人物后，使用不同颜色的编号按钮切换角色，分别调整动作、站位和体型。
- **9 张人物图**：输入 1–9 按编号对应编辑器中的人物，自动生成身份与姿势对应提示词。
- **三种操作模式**：移动人物站位、调整人物关节、移动／旋转观察视角。
- **键盘控制**：左右键转身，上下键前后移动，按住 Shift 微调。
- **209 张 OpenPose 骨架图**：点击一键摆姿；支持导入自己的骨架图片、保存与读取姿势。
- **工作流保存**：人物姿势、体型、位置和已应用的姿势参考图随工作流保存。

> 编辑器支持 9 人，并不代表生成模型能保证每次严格输出 9 个正确身份。复杂多人场景仍可能出现额外人物、身份重复或动作偏差，具体限制见下文。

## 安装

需要能够使用 `TextEncodeQwenImage21` 的 ComfyUI 版本，以及支持 WebGL 的浏览器。

在 ComfyUI 的 `custom_nodes` 目录执行：

```bash
git clone https://github.com/GStaaaaa/ComfyUI-Gaoshang-Pose.git
```

也可以在 [Releases](https://github.com/GStaaaaa/ComfyUI-Gaoshang-Pose/releases) 下载安装 ZIP，解压后把 `ComfyUI-Gaoshang-Pose` 文件夹放入 `custom_nodes`。

1. 保持文件夹名称为 **`ComfyUI-Gaoshang-Pose`**。使用 GitHub 的“Download ZIP”时，需要去掉解压目录末尾的 `-main`。
2. 完全重启 ComfyUI，然后在浏览器按 `Ctrl+Shift+R` 刷新。
3. 搜索 **“高尚姿势编辑器”** 添加节点，或拖入 [示例工作流](workflows)。

NumPy、Pillow 和 PyTorch 通常已随 ComfyUI 安装。若报缺少依赖，使用 **ComfyUI 自己的 Python 环境**执行：

```bash
python -m pip install -r requirements.txt
```

人体数据、前端依赖与 209 张骨架图已随插件附带。首次下载约 100 MB；不要删除 `web/vnccs/assets/pose_studio_makehuman.v2.bin`。

## 模型与示例工作流

插件不包含生成模型权重。示例工作流使用：

| 组件 | 示例文件 | 放置位置 |
| --- | --- | --- |
| Qwen Image 2.1 主模型 | `qwen_image_2.1_int8_convrot.safetensors` | `models/diffusion_models` |
| 文本编码器 | `qwen3vl_8b_bf16.safetensors` | `models/text_encoders` |
| VAE | `qwen_image_2.1_vae_bf16.safetensors` | `models/vae` |
| 姿势 LoRA | `VNCCS_QI2_PoseStudioV1.1.safetensors` | `models/loras` |

这些是示例所用文件名。请在各加载器中重新选择自己安装的兼容模型，并在“加载图片”节点上传自己的参考图。模型与 LoRA 的安装资料可参阅 [原项目说明](https://github.com/Work-Fisher/ComfyUI-Fisher-Pose)。

推荐从 [高尚-1-9人自由姿势编辑.json](workflows/高尚-1-9人自由姿势编辑.json) 开始。这个工作流以单人起步，后续可以添加到 9 人。

## 使用方法

1. 连接 `clip`、`vae` 和 **1号人物图片**，点击 **“打开高尚姿势编辑器”**。
2. 点击 **“添加人物”**，再通过彩色编号切换要编辑的人物。
3. 摆好每个人物的动作、大小与站位。需要整体放入输出画面时，点击 **“全部排入画框”**。
4. 点击 **“应用到节点”**。回到工作流，按编号连接同样数量的人物图片。
5. 设置输出尺寸与场景描述，然后运行工作流。

### 操作方式

| 模式 / 操作 | 作用 |
| --- | --- |
| 移动人物站位 | 鼠标左键拖动当前人物整体位置 |
| 调整人物关节 | 拖动关节调整动作 |
| 移动／旋转相框 | 左键旋转观察视角，右键或中键平移，滚轮缩放 |
| 移动模式下的 ← / → | 人物转身，每次 5° |
| 移动模式下的 ↑ / ↓ | 远离／靠近镜头 |
| Shift + 方向键 | 微调人物移动或转身 |
| 回到正面视角 | 恢复正面观察视角 |

“移动／旋转相框”改变编辑时的观察视角；模型使用的是输出画框中的正面姿势图。编辑器中的人偶图尺寸与节点最终生成尺寸可以分别设置。

### 人物输入规则

- 第 1 个人物对应 `reference_image`，第 2–9 人对应 `reference_image_2` 至 `reference_image_9`。
- 编辑器里有几个人物，就按编号连接几张人物图。不要跳过中间编号。
- 每个人物输入只接单张图片，不接图片批次。
- 模型收到的 `image1` 是姿势图，`image2` 至 `image10` 才是人物照片。
- 补充提示词建议描述背景、光线与画风；避免文字要求“全部站立”，而人偶实际处于坐姿或半跪姿。

## 已知限制

多人编辑功能已支持 1–9 人，但生成效果由模型、LoRA、参考图片与采样参数共同决定。**目前没有严格锁定输出人数、身份或关节位置的机制。**

实测五人场景中，即使输入与提示词人数正确，也可能生成六人；降低 LoRA 强度可能减少多余人物，同时削弱动作。仅强化人数提示词、合并身份图等办法尚未稳定解决这个问题。本版本保留稳定编辑器功能，没有默认启用这些实验方案。

2D OpenPose 图片不包含可靠的前后深度，导入后可能需要手动调整关节、转身与遮挡关系。

## 常见问题

**节点显示 UNKNOWN，或者找不到编辑器按钮？**

确认安装目录名称、完整重启 ComfyUI，并强制刷新浏览器。工作流使用的节点类型应为 `GaoshangQwenFreePose`。目录中应存在 `__init__.py` 和 `web/gaoshang_pose_v3.js`，不要多套一层文件夹。

**编辑器一直加载或人体模型消失？**

检查 `web/vnccs/assets/pose_studio_makehuman.v2.bin` 是否完整（约 82 MiB），以及浏览器是否可用 WebGL。

**可以与原版同时安装吗？**

本插件使用独立节点标识和前端路径。原版工作流不会自动转换为高尚版，请使用本仓库的示例工作流或手动替换节点。

## 其他节点与开发验证

包内还保留高尚机位与姿态、高尚 Qwen2.1 人物与姿态编码、GGUF CLIP 加载器。自由视角相关功能见 [详细说明](docs/自由视角详细说明.md)。GGUF 加载器需要另外安装兼容的 ComfyUI-GGUF 与相应模型。

在 ComfyUI 的 Python 环境中验证主节点（不加载模型权重）：

```bash
python tests/test_free_pose.py /path/to/ComfyUI
```

## 来源与许可证

维护者：[高尚 · GStaaaaa](https://github.com/GStaaaaa)。

本项目基于 [Work-Fisher/ComfyUI-Fisher-Pose](https://github.com/Work-Fisher/ComfyUI-Fisher-Pose) 修改，新增多人编辑、9 图输入、彩色编号、人物整体移动和模式切换等功能。保留原作者与第三方组件的版权及许可说明。

- 插件代码：见 [MIT LICENSE](LICENSE)。
- VNCCS 组件：[MIT](web/vnccs/LICENSE)。
- MakeHuman 人体资源：[CC0](web/vnccs/assets/pose_studio_makehuman.v2.CC0-1.0.md)。
- three.js：[MIT](web/editor/vendor/LICENSE)。

报错或建议请提交 [GitHub Issue](https://github.com/GStaaaaa/ComfyUI-Gaoshang-Pose/issues)，并附上 ComfyUI 版本、报错信息和可复现步骤。
