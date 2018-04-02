import os
import shutil

import appdirs
import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--ofxstatement-bin',
        action='store',
        default='ofxstatement',
        help="Full path to the 'ofxstatement' binary",
        )


@pytest.fixture
def ofxstatement_bin_path(request):
    """
    Returns the path to the 'ofxstatement' binary. The purpose of this fixture
    (and the command line option) is to allow running the integration tests
    with any installed 'ofxstatement' version.
    """
    return request.config.getoption("--ofxstatement-bin")


@pytest.fixture
def replace_config(request):
    """
    Fixture to replace the ofxstatement config file with a temporary file
    containing configuration for integration tests for this plugin. At the end
    of the test the replacement is reverted.
    """
    # Copied from 'ofxstatement' project
    APP_NAME = 'ofxstatement'
    APP_AUTHOR = 'ofx'
    cdir = appdirs.user_config_dir(APP_NAME, APP_AUTHOR)
    config_path = os.path.join(cdir, 'config.ini')
    # End of copy
    if os.path.exists(config_path):
        # Move to safe location, store backup
        backup_path = config_path + '.test.bak'
        if os.path.exists(backup_path):
            raise Exception('backup_path %s alread exists' % backup_path)
        shutil.move(config_path, backup_path)
    else:
        backup_path = None
    os.makedirs(cdir, exist_ok=True)
    with open(config_path, mode='wt', encoding='utf-8') as f:
        f.write("""\
[sparkasse_freiburg]
plugin = germany_sparkasse_freiburg
account = 333333333
            """)
    yield None
    # Cleanup (restore the original config if it existed)
    if backup_path:
        shutil.move(backup_path, config_path)
