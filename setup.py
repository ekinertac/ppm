import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip-ppm",  # Replace with your own username
    version="0.0.1",
    author="Ekin Ertaç",
    author_email="ekinertac@gmail.com",
    description="A pip alternative for managing python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ekinertac/ppm",
    packages=['ppm'],
    scripts=['bin/ppm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click==7.0',
        'pip-api==0.0.13'
    ],
    python_requires='>=3.6',
)
