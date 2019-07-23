import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IPGeoSearch",
    version="1.0.0",
    author="Matthias Rathbun, Cyber Threat Intelligence Lab",
    author_email="matthiasrathbun@gmail.com",
    python_requires='>=3.6',
    description="IPGeo-Search is a python module which allows for easy use of the IPGeo API. It allows both free and paid users to send requests to the server in just one line of code, allowing for customization of how IP lists are loaded.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas'],
    url="http://ipgeo.azurewebsites.net/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)