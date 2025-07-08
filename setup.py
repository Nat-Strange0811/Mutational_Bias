from setuptools import setup

APP = ['main.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'includes': ['tkinter'],
    'packages': ['Bio', 'numpy', 'appdirs'],
    'resources': [],
    'plist': {
        'CFBundleName': 'MyBioApp',
        'CFBundleDisplayName': 'MyBioApp',
        'CFBundleIdentifier': 'com.yourname.mybioapp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)