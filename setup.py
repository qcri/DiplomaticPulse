"""Module to setup the library. All library dependencies are added here.
"""
from setuptools import setup, find_packages

setup(name="diplomaticpulse",
      author="QCRI",
      author_email="alattab@hbku.edu.qa",
      long_description="long_description",
      long_description_content_type="text/markdown",
      url="https://github.com/qcri/DiplomaticPulse",
      version='1.0.0',
      license=" BSD-3-Clause",
      description='Scrapy crawlers which allow you to crawl, scrape and store html contents in Elasticsearch.',
      packages=find_packages(),
      include_package_data=True,
      package_data = {
          "diplomaticpulse": ["*.txt",],
      },
      platforms = ['Any'],
      install_requires = ['pyes', 'scrapy'],
      entry_points = {'scrapy': ['settings = diplomaticpulse.settings']},
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Environment :: No Input/Output (Daemon)',
                      'License :: OSI Approved :: Apache Software License',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python']
      )

