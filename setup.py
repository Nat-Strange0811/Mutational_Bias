from setuptools import setup

APP = ['main.py']
DATA_FILES = ['Database/CpG_data.db']

OPTIONS = {
    'argv_emulation': True,
    'includes': ['tkinter', 'sqlite3', 'os', 'shutil', 'pathlib', 'psycopg2', 'psycopg2._psycopg', 'decimal'],
    'packages': ['Bio', 'numpy', 'appdirs', 'psycopg2'],
    'resources': ['Database'],
    'compressed': False,
    'plist': {
        'CFBundleName': 'Mutational Bias',
        'CFBundleDisplayName': 'Mutational Bias',
        'CFBundleIdentifier': 'com.yourname.mutationalbias',
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