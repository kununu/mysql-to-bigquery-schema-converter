import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysql-to-bigquery-schema-converter",
    version="0.0.1",
    author="Lorenzo Alfine",
    author_email="lorenzo.alfine@kununu.com",
    description="MySql to BigQuery schema converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kununulabs/mysql-to-bigquery-schema-converter",
    packages=setuptools.find_packages('converter'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
