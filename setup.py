from setuptools import setup

APP = ['main.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'includes': ['Bio', 'numpy', 'tkinter'],  # Use 'includes' instead of 'packages'
    'packages': [],  # Leave empty unless you're bundling folders/modules
    'plist': {
        'CFBundleName': 'MyBioApp',
        'CFBundleDisplayName': 'MyBioApp',
        'CFBundleIdentifier': 'com.yourname.mybioapp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    },
    'resources': [],  # Add data files if needed
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)