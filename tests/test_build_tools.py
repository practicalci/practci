
import os
import shutil
import unittest


from practci import build_tools
from practci.build_tools import BuildToolType, BuildTarget, BuildType

from practci import toolchains

from tests.project_templates import cmake as cmake_template


class TestBuildTool(unittest.TestCase):

    def test_get_build_tool(self):
        build_tool = build_tools.get_build_tool(BuildToolType.CMAKE)
        self.assertIsNotNone(build_tool)

    def test_build_setup_cmake(self):
        build_tool = build_tools.get_build_tool(BuildToolType.CMAKE)

        template_project_root_dir = os.path.dirname(cmake_template.__file__)

        toolchain = toolchains.get_tool_chain('native/identity', template_project_root_dir)

        build_tool.setup(project_root_dir=template_project_root_dir, toolchain=toolchain, build_type=BuildType.DEBUG,
                         )

        build_dir = os.path.join(template_project_root_dir, 'build')

        self.assertTrue(os.path.exists(build_dir))
        self.assertTrue(os.path.isdir(build_dir))

        shutil.rmtree(build_dir)

    def test_build_purge_cmake(self):

        build_tool = build_tools.get_build_tool(BuildToolType.CMAKE)

        template_project_root_dir = os.path.dirname(cmake_template.__file__)

        toolchain = toolchains.get_tool_chain('native/identity', template_project_root_dir)

        build_dir = os.path.join(template_project_root_dir, 'build')
        install_dir = os.path.join(template_project_root_dir, 'install')

        build_tool.setup(project_root_dir=template_project_root_dir, toolchain=toolchain, build_type=BuildType.DEBUG)

        self.assertTrue(os.path.exists(build_dir))
        self.assertTrue(os.path.exists(install_dir))

        build_tool.purge(project_root_dir=template_project_root_dir, toolchain=toolchain)

        build_dir = os.path.join(template_project_root_dir, 'build', toolchain.get_name())
        install_dir = os.path.join(template_project_root_dir, 'install', toolchain.get_name())

        self.assertFalse(os.path.exists(build_dir))
        self.assertFalse(os.path.exists(install_dir))

    def test_build_purge__all_cmake(self):

        build_tool = build_tools.get_build_tool(BuildToolType.CMAKE)

        template_project_root_dir = os.path.dirname(cmake_template.__file__)

        toolchain = toolchains.get_tool_chain('native/identity', template_project_root_dir)

        build_dir = os.path.join(template_project_root_dir, 'build')
        install_dir = os.path.join(template_project_root_dir, 'install')

        build_tool.setup(project_root_dir=template_project_root_dir, toolchain=toolchain, build_type=BuildType.DEBUG)

        self.assertTrue(os.path.exists(build_dir))
        self.assertTrue(os.path.exists(install_dir))

        build_tool.purge_all(project_root_dir=template_project_root_dir)

        self.assertFalse(os.path.exists(build_dir))
        self.assertFalse(os.path.exists(install_dir))
