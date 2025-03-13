from setuptools import setup, find_packages

setup(
    name="pawse",
    version="1.0.0",
    description="A cat typing detector and blocker for macOS",
    author="Alina",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pawse",
    packages=find_packages(),
    install_requires=[
        "rumps>=0.4.0",
        "pyobjc>=9.2",
        "playsound>=1.3.0",
    ],
    package_data={
        "pawse": ["meow.mp3", "pawse_icon.png"],
    },
    entry_points={
        "console_scripts": [
            "pawse=pawse_menu:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
) 