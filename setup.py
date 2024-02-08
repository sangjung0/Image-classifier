import io
from setuptools import find_packages, setup
from project_constants import PROJECT_NAME, PROJECT_VERSION, PROJECT_DESCRIPTION, PROJECT_AUTHOR, PROJECT_URL, PROJECT_AUTHOR_EMAIL


def long_description():
    with io.open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

setup(name=PROJECT_NAME,
      version=PROJECT_VERSION,
      description=PROJECT_DESCRIPTION,
      long_description=long_description(),
      url= PROJECT_URL,
      author=PROJECT_AUTHOR,
      author_email= PROJECT_AUTHOR_EMAIL,
      license='MIT',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3.9',
          ],
      python_requires = "<=3.9",
      zip_safe=False)