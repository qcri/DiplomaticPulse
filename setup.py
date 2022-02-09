from setuptools import setup, find_packages

setup(name='diplomaticpulse',
      version='0.1.199',
      license='Apache License, Version 2.0',
      description='Scrapy pipeline which allow you to store scrapy items in Elastic Search.',
      author='Julien Duponchelle',
      author_email='julien@duponchelle.info',
      url='http://github.com/noplay/scrapy-elasticsearch',
      keywords="scrapy elastic search",
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
