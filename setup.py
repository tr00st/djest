from setuptools import setup # pragma: no cover 

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()] # pragma: no cover

setup(name='Djest',
      version='0.1',
      packages=['djest'],
      cmdclass={'upload':lambda x:None},
      install_requires=[
          'django',
          'beautifulsoup4'
      ],
      dependency_links=REQUIREMENTS,
      use_2to3 = True,
      )# pragma: no cover 
 
 
