import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cybertnetica",
    version="0.0.1",
    author="roventine",
    author_email="ukyotachibana@yeah.net",
    description="automata for deployment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roventine/cybertnetica",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['paramiko', 'pywildcard', 'logbook','pyyaml'],
)
