from setuptools import setup, find_namespace_packages

# Constants
PROJECT_NAME = "pygatekeeper"
PROJECT_VERSION = "1.0.1"
AUTHOR = ["Jeetendra Gupta", "jeetendra29gupta@gmail.com"]
DESCRIPTION = "A Python-based authentication and access control system."

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PROJECT_NAME,
    version=PROJECT_VERSION,
    author=AUTHOR[0],
    author_email=AUTHOR[1],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jeetendra29/pygatekeeper',
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    install_requires=[
        'bcrypt',
        'pyjwt',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    keywords='authentication security access-control python',
    python_requires='>=3.8',
)
