
import io
import os
import unittest


from practci import toolchains

from tests.project_templates import cmake as cmake_template
from tests import scripts

class TestToolChains(unittest.TestCase):
    """Tests for `practci.ToolChains` class."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_toolchain(self):
        toolchain = toolchains.get_tool_chain('native/gcc')
        self.assertIsNotNone(toolchain)

    def test_get_toolchain_channel(self):
        toolchain = toolchains.get_tool_chain('native/gcc')
        self.assertIsNotNone(toolchain.get_channel())
        self.assertEqual(toolchain.get_channel(), 'native')

    def test_get_wrapper_script_name(self):
        toolchain = toolchains.get_tool_chain('native/gcc')
        self.assertIsNotNone(toolchain.get_wrapper_script_name())
        self.assertEqual(toolchain.get_wrapper_script_name(), 'gcc')

    def test_get_wrapper_script_path(self):
        toolchain = toolchains.get_tool_chain('native/identity')
        self.assertIsNotNone(toolchain.get_wrapper_script_path())
        self.assertEqual(toolchain.get_wrapper_script_path(), '.practci/bin/toolchains/native/linux/identity')

    def test_get_wrapper_script_abs_path(self):
        toolchain = toolchains.get_tool_chain('native/identity')
        template_project_root_dir = os.path.dirname(cmake_template.__file__)
        self.assertEqual(toolchain.get_wrapper_script_abs_path(project_root_dir=template_project_root_dir),
                         os.path.join(template_project_root_dir,'.practci/bin/toolchains/native/linux/identity'))


    def test_is_installed(self):
        toolchain = toolchains.get_tool_chain('native/identity', os.path.dirname(cmake_template.__file__))
        self.assertTrue(toolchain.is_installed())

    def test_not_is_installed(self):
        toolchain = toolchains.get_tool_chain('native/none', os.path.dirname(cmake_template.__file__))
        self.assertFalse(toolchain.is_installed())

    def test_exec_command(self):
        toolchain = toolchains.get_tool_chain('native/identity', os.path.dirname(cmake_template.__file__))

        template_project_root_dir = os.path.dirname(cmake_template.__file__)

        command_output_stream = io.StringIO()
        toolchain.exec_command(['echo', '-n', 'I am a master command!'], project_root_dir=template_project_root_dir,
                               stdout=command_output_stream)

        self.assertEqual('I am a master command!', command_output_stream.getvalue())

    def test_fail_exec_command(self):
        toolchain = toolchains.get_tool_chain('native/identity', os.path.dirname(cmake_template.__file__))

        template_project_root_dir = os.path.dirname(cmake_template.__file__)

        command = os.path.join(os.path.dirname(scripts.__file__), 'fail_script.sh')

        command_err_stream = io.StringIO()

        try:
            toolchain.exec_command([command], project_root_dir=template_project_root_dir,
                                   stderr=command_err_stream)
        except toolchains.ToolChainExecFail:
            pass
        except Exception as ex:
            self.fail(ex)
        else:
            self.fail()

        self.assertEqual('I am a master error!', command_err_stream.getvalue())
