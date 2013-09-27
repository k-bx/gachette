import unittest
import mock

from gachette.lib.stack import Stack


class StackTest(unittest.TestCase):
    def setUp(self):
        self.stack = Stack('1.0.0', meta_path='/var/gachette')

    def tearDown(self):
        self.stack = None

    @mock.patch('gachette.lib.stack.run')
    def test_stack(self, stack_run_mock):
        name = 'app'
        version = '1.1.1'
        file_name = 'app-1.1.1.deb'

        self.stack.add_package(name, version, file_name)

        pkg_folder_dst = "/var/gachette/packages/%s/version/%s" % \
                                                    (name, version)
        stack_folder_dst = "/var/gachette/stacks/%s/packages/%s" % \
                                                    (self.stack.version, name)

        stack_run_mock.assert_has_calls(
                                [mock.call("mkdir -p %s" % pkg_folder_dst),
                                 mock.call("echo %s > %s/file" % (file_name,
                                                                  pkg_folder_dst)),
                                 mock.call("mkdir -p %s" % stack_folder_dst),
                                 mock.call("echo %s > %s/version" % (version,
                                                                     stack_folder_dst))])



if __name__ == "__main__":
    unittest.main()