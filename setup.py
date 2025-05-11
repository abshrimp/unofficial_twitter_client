from setuptools import setup, find_packages

setup(
    name="unofficial_twitter_client",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests-oauthlib>=1.3.1",
        "requests>=2.31.0",
    ],
    author="abshrimp",
    author_email="abshrimps@gmail.com",
    description="Unofficial Twitter Client API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abshrimp/unofficial_twitter_client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
) 