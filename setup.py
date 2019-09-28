from setuptools import setup, find_packages

install_requires = ['numpy', 'pandas', 'seaborn', 'matplotlib', 'statsmodels']

setup(name='',
      version='0.0.1',
      description='Tools for exploratory data analysis',
      author='Jonghwan Yoo',
      author_email='yjh3620@ad.unc.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=install_requires,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
