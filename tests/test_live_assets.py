"""Check the installed plugin through the running ComfyUI server, not a file server."""
import json
import unittest
from urllib.request import urlopen

BASE = 'http://127.0.0.1:8188'
PREFIX = '/extensions/ComfyUI-Gaoshang-Pose'


class InstalledAssetsTests(unittest.TestCase):
    def test_registered_node_and_extension_are_reachable(self):
        with urlopen(BASE + '/object_info/GaoshangQwenFreePose', timeout=10) as response:
            node = json.load(response)['GaoshangQwenFreePose']
        self.assertEqual(node['python_module'], 'custom_nodes.ComfyUI-Gaoshang-Pose')
        self.assertEqual(len(node['input']['optional']), 8)
        with urlopen(BASE + '/extensions', timeout=10) as response:
            scripts = json.load(response)
        script = PREFIX + '/gaoshang_pose_v3.js'
        self.assertIn(script, scripts)
        for path in [script, PREFIX + '/editor/freepose.mjs', PREFIX + '/vnccs/vnccs_pose_studio_core.mjs']:
            with self.subTest(path=path), urlopen(BASE + path, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertIn('javascript', response.headers['Content-Type'])
        with urlopen(BASE + PREFIX + '/editor/freepose.html', timeout=10) as response:
            self.assertIn('data-edit-mode="move"', response.read().decode())

    def test_gallery_route_is_registered(self):
        with urlopen(BASE + '/gaoshang_pose/builtin_poses', timeout=10) as response:
            self.assertEqual(len(json.load(response)['files']), 209)


if __name__ == '__main__':
    unittest.main()
