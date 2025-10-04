from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="advanced-file-sorter",
    version="1.0.0",
    author="Syed Dayim",
    author_email="dayim1277@gmail.com",
    description="An advanced file sorting application with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syedDayim/advanced-file-sorter",
    project_urls={
        "Bug Tracker": "https://github.com/syedDayim/advanced-file-sorter/issues",
        "Source Code": "https://github.com/syedDayim/advanced-file-sorter",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment :: File Managers",
        "Topic :: System :: Filesystems",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyinstaller>=5.0",
    ],
    entry_points={
        "console_scripts": [
            "file-sorter=fileSorter:main",
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
