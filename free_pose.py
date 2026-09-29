"""Gaoshang 1–9 person editor, based on 高尚/VNCCS.

Single-person mode preserves the original VNCCS LoRA instruction. Multi-person
mode binds fixed mannequin colors to ordered character references.
"""
import json
import numpy as np
import torch

from .pose_reference import reference_image

VNCCS_INSTRUCTION = "Draw character from image2"


def free_pose_prompt(extra=""):
    lines = [VNCCS_INSTRUCTION] + [line.strip() for line in str(extra or "").splitlines()]
    return "\n".join(line for line in lines if line)


def mannequin_tensor(pose_json):
    # The mannequin keeps the size chosen in the editor; the node's width/height only set the output latent.
    return torch.from_numpy(np.asarray(reference_image(pose_json)).astype(np.float32) / 255).unsqueeze(0)


class GaoshangQwenFreePose:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "clip": ("CLIP",), "vae": ("VAE",), "reference_image": ("IMAGE",),
            "width": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 16}),
            "height": ("INT", {"default": 1024, "min": 64, "max": 4096, "step": 16}),
            "reference_resolution": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 32}),
            "extra_prompt": ("STRING", {"default": "", "multiline": True}),
            "pose_json": ("STRING", {"default": "{}", "multiline": True}),
        }, "optional": {f"reference_image_{i}": ("IMAGE", {"tooltip": f"{i}号人物参考图"}) for i in range(2, 10)}}

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "LATENT", "STRING", "IMAGE")
    RETURN_NAMES = ("正向", "负向", "latent", "实际提示词", "人偶姿态图")
    FUNCTION = "encode"
    CATEGORY = "高尚/姿态与机位"
    DESCRIPTION = "高尚姿势编辑器：1–9 人独立摆姿、站位和体型。reference_image 为1号人物，其余输入按编号对应。姿势图为 image1，人物图为 image2–image10。单人保留原 LoRA 指令；多人按颜色绑定身份。"

    def encode(self, clip, vae, reference_image, width, height, reference_resolution, extra_prompt, pose_json, **references):
        if width % 16 or height % 16:
            raise ValueError("Qwen 输出宽高须为16的倍数，请调整节点的 width/height。")
        refs = [reference_image] + [references.get(f"reference_image_{i}") for i in range(2, 10)]
        state = json.loads(pose_json)
        people = state.get("people")
        count = len(people) if isinstance(people, list) else 1
        if not 1 <= count <= 9:
            raise ValueError("高尚姿势编辑器支持 1 到 9 个人物。")
        if any(refs[i] is None for i in range(count)):
            raise ValueError(f"当前姿势有 {count} 人，请按编号连接 1 到 {count} 号人物图片。")
        if any(image is not None for image in refs[count:]):
            raise ValueError("人物图片多于编辑器中的人数，请打开高尚姿势编辑器添加对应人物。")
        refs = refs[:count]
        if any(image.ndim != 4 or image.shape[0] != 1 for image in refs):
            raise ValueError("每个人物输入只能连接单张图片，不支持图片批次。")
        mannequin = mannequin_tensor(pose_json)
        prompt = free_pose_prompt(extra_prompt)
        if count > 1:
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'pink', 'brown']
            lines = [f"Create one coherent scene with exactly {count} people. Use image1 as the pose and composition guide."]
            lines += [f"Person {i+1}: replace the {colors[i]} mannequin in image1 with the character from image{i+2}. Preserve that character's face, hairstyle and clothing; match that mannequin's pose, position, scale and facing direction." for i in range(count)]
            lines += ["Keep all identities separate. Render natural people, without mannequin colors, labels or extra people.", str(extra_prompt).strip()]
            prompt = "\n".join(line for line in lines if line)
        try:
            from comfy_extras.nodes_qwen import TextEncodeQwenImage21
        except ImportError as error:
            raise RuntimeError("此节点需要包含 TextEncodeQwenImage21 的新版 ComfyUI。") from error
        result = TextEncodeQwenImage21.execute(clip=clip, prompt=prompt, negative_prompt="", vae=vae,
                    resolution=reference_resolution, images={f"image_{i+1}": image for i, image in enumerate([mannequin] + refs)})
        positive, negative, encoded_latent = result.result
        # Output size comes from the node, independent of the mannequin (the encoder would size it from image1).
        latent = {"samples": encoded_latent["samples"].new_zeros((1, 64, height // 16, width // 16))}
        return {"ui": {"gaoshang_prompt": [prompt]}, "result": (positive, negative, latent, prompt, mannequin)}
