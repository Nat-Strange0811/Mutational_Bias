from setuptools import setup

APP = ['main.py']
DATA_FILES = ['Database/CpG_data.db']

OPTIONS = {
    'argv_emulation': True,
    'includes': ['tkinter'],
    'packages': ['Bio', 'numpy', 'appdirs'],
    'resources': ['Database/CpG_data.db'],
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