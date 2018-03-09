from setuptools import find_packages, setup


setup(
    name="docconvert",
    version="1.1.0",
    description="Convert and conform package docstrings to a new style.",
    package_dir={"": "src"},
    packages=find_packages("src"),
    tests_require=[
        "pytest",
    ],
    install_requires=[
        'enum34;python_version<"3.4"',
        "six",
    ],
    entry_points={
        "console_scripts": ["docconvert = docconvert.cli:run"]
    },
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    classifiers=[
        "Development Status :: 5 - Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
