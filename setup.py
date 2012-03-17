from setuptools import setup, find_packages

def read(fname):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='epostkr',
      version='0.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      license='GNU Affero GPL v3',
      description='a client for epost.kr OpenAPI',
      long_description=read('README.txt'),
      author='mete0r',
      author_email='mete0r@sarangbang.or.kr',
      entry_points={
          'console_scripts':[
              'epostkr-zipcode = epostkr:find_zipcodes'
          ]},
      classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU Affero General Public License v3',
          'Natural Language :: English',
          'Natural Language :: Korean',
          'Programming Language :: Python',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities',
      ])
