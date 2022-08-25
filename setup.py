"""Setup package for building"""
import sys
import setuptools
import versioneer

# Add the current directory to path so versioneer is found (see
# https://github.com/python-versioneer/python-versioneer/issues/249) as python -m build triggers a build compliant with
# PEP517 and PEP518 even though config explicitly states to use PEP440. It may have been fixed recently with
# https://github.com/python-versioneer/python-versioneer/pull/294 but a new release is pending
sys.path.insert(0, ".")
setuptools.setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
