"""Test cases that run tests as subprocesses."""

from typing import List

import os
import subprocess
import sys
import unittest


base_dir = os.path.join(os.path.dirname(__file__), '..', '..')


class TestExternal(unittest.TestCase):
    # TODO: Get this to work on Windows.
    # (Or don't. It is probably not a good use of time.)
    @unittest.skipIf(sys.platform.startswith("win"), "rt tests don't work on windows")
    def test_c_unit_test(self) -> None:
        """Run C unit tests in a subprocess."""
        # Build Google Test, the C++ framework we use for testing C code.
        # The source code for Google Test is copied to this repository.
        cppflags = []  # type: List[str]
        env = os.environ.copy()
        if sys.platform == 'darwin':
            cppflags += ['-mmacosx-version-min=10.10', '-stdlib=libc++']
        env['CPPFLAGS'] = ' '.join(cppflags)
        subprocess.check_call(['make', 'libgtest.a'],
                              env=env,
                              cwd=os.path.join(base_dir, 'external', 'googletest', 'make'))
        # Build Python wrapper for C unit tests.
        env = os.environ.copy()
        env['CPPFLAGS'] = ' '.join(cppflags)
        status = subprocess.check_call(
            [sys.executable, 'setup.py', 'build_ext', '--inplace'],
            env=env,
            cwd=os.path.join(base_dir, 'mypyc', 'lib-rt'))
        # Run C unit tests.
        env = os.environ.copy()
        if 'GTEST_COLOR' not in os.environ:
            env['GTEST_COLOR'] = 'yes'  # Use fancy colors
        status = subprocess.call([sys.executable, '-c',
                                  'import sys, test_capi; sys.exit(test_capi.run_tests())'],
                                 env=env,
                                 cwd=os.path.join(base_dir, 'mypyc', 'lib-rt'))
        if status != 0:
            raise AssertionError("make test: C unit test failure")

    def test_self_type_check(self) -> None:
        """Use the bundled mypy (in git submodule) to type check mypyc."""
        mypy_dir = os.path.join(base_dir, 'mypyc', 'external', 'mypy')
        if not os.path.exists(os.path.join(mypy_dir, 'mypy', 'typeshed', 'stdlib')):
            raise AssertionError('Submodule mypy/mypy/typeshed not ready')
        env = os.environ.copy()
        env['PYTHONPATH'] = mypy_dir
        env['MYPYPATH'] = os.pathsep.join((mypy_dir, base_dir))
        status = subprocess.call(
            [sys.executable,
             '-m', 'mypy',
             '--config-file', 'mypy.ini', '-p', 'mypyc'],
            env=env)
        if status != 0:
            raise AssertionError("Self type check failure")

    def test_flake8(self) -> None:
        """Use flake8 to lint mypyc."""
        status = cached_flake8('mypyc')
        if status != 0:
            assert False, "Lint failure"


CACHE_FILE = '.mypyc-flake8-cache.json'


def cached_flake8(dir: str) -> int:
    """Run flake8 with cached results from the previous clean run.

    Record the hashes of files after a clean run and don't pass the files to
    flake8 if they have the same hashes, as they are expected to produce a
    clean output.

    If flake8 settings or version change, the cache file may need to be manually
    removed.
    """
    import hashlib
    import glob
    import json

    if os.path.isfile(CACHE_FILE):
        with open(CACHE_FILE) as f:
            cache = json.load(f)
    else:
        cache = {}
    files = glob.glob('%s/**/*.py' % dir, recursive=True)
    files = [f for f in files if not f.startswith(os.path.join(dir, 'external', 'mypy'))]
    hashes = {}
    for fn in files:
        with open(fn, 'rb') as fb:
            data = fb.read()
        hashes[fn] = hashlib.sha1(data).hexdigest()
    filtered = [fn for fn in files
                if hashes[fn] != cache.get(fn)]
    if not filtered:
        # Nothing has changed since the previous clean run -- must be clean.
        return 0
    status = subprocess.call([sys.executable, '-m', 'flake8'] + filtered)
    if status == 0:
        for fn, sha in hashes.items():
            cache[fn] = sha
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=4)
    return status
