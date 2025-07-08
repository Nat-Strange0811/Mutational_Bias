from setuptools import setup

APP = ['main.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'includes': ['Bio', 'numpy'],  # Use 'includes' instead of 'packages'
    'packages': [],  # Leave empty unless you're bundling folders/modules
    'excludes': ['tkinter'],  # Exclude if not used (py2app might try to include)
    'iconfile': 'icon.icns',  # Optional: only if you have a custom icon
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