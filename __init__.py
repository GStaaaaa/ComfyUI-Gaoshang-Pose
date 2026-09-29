from .nodes import GaoshangPoseStudio
from .qwen_bridge import GaoshangQwenPose
from .gguf_clip import GaoshangQwen21GGUFCLIP
from .free_pose import GaoshangQwenFreePose
from .openpose_library import register_routes
from .saved_poses import register_routes as register_saved_pose_routes

register_routes()
register_saved_pose_routes()

NODE_CLASS_MAPPINGS = {"GaoshangPoseStudio": GaoshangPoseStudio, "GaoshangQwenPose": GaoshangQwenPose}
NODE_DISPLAY_NAME_MAPPINGS = {"GaoshangPoseStudio": "高尚机位与姿态", "GaoshangQwenPose": "高尚 Qwen2.1 人物与姿态编码"}
NODE_CLASS_MAPPINGS['GaoshangQwen21GGUFCLIP'] = GaoshangQwen21GGUFCLIP
NODE_CLASS_MAPPINGS['GaoshangQwenFreePose'] = GaoshangQwenFreePose
NODE_DISPLAY_NAME_MAPPINGS['GaoshangQwenFreePose'] = '高尚姿势编辑器'
NODE_DISPLAY_NAME_MAPPINGS['GaoshangQwen21GGUFCLIP'] = '高尚 Qwen2.1 GGUF CLIP加载器'
WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
