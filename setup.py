import setuptools

REQUIRES = [
    'numpy',
    'tqdm',
    'psutil',
    'scipy',
    'matplotlib',
    'fuzzywuzzy',
    'parallelencode'
]

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="parallelencodecli",
    version="0.1.3",
    author="Parallel Encoders",
    author_email="eli.stonium@gmail.com",
    description="Parallel encoding cli interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parallelencode/pecli",
    packages=setuptools.find_packages('.', exclude='tests'),
    install_requires=REQUIRES,
    py_modules=['pecli'],
    entry_points={"console_scripts": ["pecli=pecli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
