
import os
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

        build_tool.build(project_root_dir=template_project_root_dir,
                         target=BuildTarget.SETUP_BUILD, build_type=BuildType.DEBUG,
                         toolchain=toolchain, checkchain=toolchain)

        self.assertTrue(os.path.exists(os.path.join(template_project_root_dir, 'build')))
        self.assertTrue(os.path.isdir(os.path.join(template_project_root_dir, 'build')))


