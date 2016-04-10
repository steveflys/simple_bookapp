from setuptools import setup

setup(
    name='simple-bookapp',
    version='0.1',
    description='A simple WSGI book list application',
    author='Cris Ewing',
    author_email='cris@crisewing.com',
    license='MIT',
    package_dir={'': 'src'},
    py_modules=['bookapp', 'bookdb'],
    install_requires=[],
    extras_require={'test': ['pytest', 'pytest-watch', 'webtest', 'tox']},
)
