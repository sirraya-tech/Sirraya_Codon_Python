from setuptools import setup, find_packages

setup(
    name="sirraya-codon-sdk",
    version="0.1.0",
    description="Sirraya Codon SDK - Secure AI/ML/IoT Command Encoding and Parsing",
    author="Amir Hameed",
    author_email="amir@example.com",  # Replace with your email
    url="https://github.com/sirraya-tech/sirraya-codon-python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psutil==5.9.5",
        "spacy==3.5.4",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
