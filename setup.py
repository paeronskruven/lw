import os
from setuptools import setup, find_packages
from setuptools.command.install import install


class CustomInstall(install):

    def run(self):
        install.run(self)

        for filepath in self.get_outputs():
            if os.path.expanduser('~/.lw') in filepath:
                os.chmod(os.path.dirname(filepath), 0o777)


setup(
    name='ListingsWatch',
    packages=find_packages(),
    version='1.0',
    description='Command line application watching listings for keywords',
    author='Tommy Lundgren',
    author_email='tomolia86@yahoo.se',
    install_requires=['beautifulsoup4'],
    entry_points = {
        'console_scripts': ['lw = lw.__main__:main']
    },
    data_files=[
        (os.path.expanduser('~/.lw'), ['lw.conf'])
    ],
    cmdclass={'install': CustomInstall}
)
