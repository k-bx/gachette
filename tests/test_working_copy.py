import os
import unittest
import mock

from gachette.lib.working_copy import WorkingCopy


class GitVersionTest(unittest.TestCase):
    def setUp(self):
        self.wc = WorkingCopy("version_test")

    def tearDown(self):
        self.wc = None

    @mock.patch('gachette.lib.working_copy.get_current_git_hash', return_value="1A2B3C4D")
    def test_basic(self, git_hash_mock):
        version = self.wc.get_version_from_git()
        self.assertEqual(version,
                        '0.0.1rev1A2B3C4D',
                        "Wrong version given %s" % version)

        version = self.wc.get_version_from_git(suffix="foo")
        self.assertEqual(version,
                        '0.0.1rev1A2B3C4D-foo',
                        "Wrong version given %s" % version)

        version = self.wc.get_version_from_git(suffix="foo_bar")
        self.assertEqual(version,
                        '0.0.1rev1A2B3C4D-foo-bar',
                        "Wrong version given %s" % version)

class VersionTest(unittest.TestCase):
    def setUp(self):
        self.wc = WorkingCopy("version_test")

    def tearDown(self):
        self.wc = None

    def test_app_version(self):
        self.wc.set_version(app='1.2.3')
        self.assertEqual(self.wc.get_version_suffix(), " --app-version 1.2.3", 
                        "app version is not well recognized (%s)" % self.wc.get_version_suffix())

        self.wc.set_version(app='1.2.4')
        self.assertEqual(self.wc.get_version_suffix(), " --app-version 1.2.4", 
                        "app version is updated properly (%s)" % self.wc.get_version_suffix())

        self.wc.set_version(app='')
        self.assertEqual(self.wc.get_version_suffix(), "",
                        "app version is removed properly (%s)" % self.wc.get_version_suffix())

    def test_env_version(self):
        self.wc.set_version(env='1.2.3')
        self.assertEqual(self.wc.get_version_suffix(), " --env-version 1.2.3", 
                        "env version is not well recognized (%s)" % self.wc.get_version_suffix())

    def test_service_version(self):
        self.wc.set_version(service='1.2.3')
        self.assertEqual(self.wc.get_version_suffix(), " --service-version 1.2.3", 
                        "service version is not well recognized (%s)" % self.wc.get_version_suffix())

    def test_multiple_version(self):
        self.wc.set_version(app='1.2.3')
        self.wc.set_version(env='2.3.4')
        self.assertEqual(self.wc.get_version_suffix(), " --app-version 1.2.3 --env-version 2.3.4",
                        "env and app version are not well recognized (%s)" % self.wc.get_version_suffix())
        self.wc.set_version(service='3.4.5')
        self.assertEqual(self.wc.get_version_suffix(), " --app-version 1.2.3 --env-version 2.3.4 --service-version 3.4.5",
                        "service, env and app version are not well recognized (%s)" % self.wc.get_version_suffix())

    def test_all_version(self):
        self.wc.set_version(service='3.4.5')
        self.wc.set_version(app='1.2.3')
        self.wc.set_version(env='2.3.4')
        self.assertEqual(self.wc.get_version_suffix(), " --app-version 1.2.3 --env-version 2.3.4 --service-version 3.4.5", 
                        "service, env and app version are sorted properly (%s)" % self.wc.get_version_suffix())


class run_failed(object):
    def __init__(self, return_value):
        self.return_value = return_value

    @property
    def failed(self):
        return self.return_value


class PrepareTest(unittest.TestCase):
    def setUp(self):
        self.wc = WorkingCopy("prepare_test")

    def tearDown(self):
        self.wc = None

    @mock.patch('gachette.lib.utils.run', return_value=run_failed(True))
    def test_prepare_environment_default(self, utils_run_mock):
        """
        Prepare not existing folder
        """
        folder = self.wc.working_copy
        self.wc.prepare_environment()

        utils_run_mock.assert_has_calls(
                                [mock.call("test -d %s" % folder),
                                 mock.call("mkdir -p %s" % folder)])

    @mock.patch('gachette.lib.utils.run', return_value=run_failed(False))
    def test_prepare_environment_existing(self, utils_run_mock):
        """
        Prepare existing folder
        """
        folder = self.wc.working_copy
        self.wc.prepare_environment()

        utils_run_mock.assert_has_calls(
                            [mock.call("test -d %s" % folder),
                             mock.call("rm -rf %s/*" % folder)])

    @mock.patch('gachette.lib.working_copy.run', return_value=run_failed(True))
    def test_checkout_clone(self, fabric_run_mock):
        # This URL does not exist. For test only
        folder = self.wc.working_copy
        url = 'https://github.com/organizations/gachette/test_project'
        branch = 'test-branch'
        self.wc.checkout_working_copy(url, branch)

        fabric_run_mock.assert_has_calls(
                [mock.call('test -d %s/.git' % folder),
                 mock.call('git clone --depth=100 --quiet %s %s' % (url, folder)),
                 mock.call('git fetch --quiet origin'),
                 mock.call('git reset --quiet --hard origin/%s' % branch),
                 mock.call('git submodule --quiet init'),
                 mock.call('git submodule --quiet update'),
                 mock.call('git rev-parse HEAD')])

    @mock.patch('gachette.lib.working_copy.run', return_value=run_failed(False))
    def test_checkout_update(self, fabric_run_mock):
        # This URL does not exist. For test only
        folder = self.wc.working_copy
        url = 'https://github.com/organizations/gachette/test_project'
        branch = 'test-branch'
        self.wc.checkout_working_copy(url, branch)

        fabric_run_mock.assert_has_calls(
                [mock.call('test -d %s/.git' % folder),
                 mock.call('git fetch --quiet origin'),
                 mock.call('git reset --quiet --hard origin/%s' % branch),
                 mock.call('git submodule --quiet init'),
                 mock.call('git submodule --quiet update'),
                 mock.call('git rev-parse HEAD')])


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.wc = WorkingCopy("build_test")

    def tearDown(self):
        self.wc = None

    @mock.patch('gachette.lib.working_copy.run')
    def test_build(self, fabric_run_mock):
        app_version = '1.1.0'
        webcallback = 'http://garnison.dev:8080/stacks/1234/build_cb'
        self.wc.set_version(app=app_version)
        self.wc.build('/var/gachette/debs', webcallback=webcallback)

        fabric_run_mock.assert_has_calls(
                [mock.call('trebuchet build %s --arch amd64 --output %s %s %s' \
                    % (os.path.join(self.wc.working_copy, '.missile.yml'),
                       '/var/gachette/debs',
                       self.wc.get_version_suffix(),
                       self.wc.get_webcallback_suffix(webcallback)))])


if __name__ == '__main__':
    unittest.main()
