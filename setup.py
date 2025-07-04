from setuptools import setup

APP = ['main.py']  # Your main script
OPTIONS = {
    'argv_emulation': True,
    'packages': ['Bio', 'numpy'],
    'plist': {
        'CFBundleName': 'MyBioApp',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.yourname.mybioapp',
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)