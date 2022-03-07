from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='d365fo_tools',
    version='1.0.0.1',
    description='Basic tools for D365FO.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arnaldo Ono',
    author_email='git@onoarnaldo.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],

    keywords='d365fo, development',
    package_dir={'': 'src', 'd365fo_tools': 'src/d365fo_tools'},
    packages=find_packages(where='src'),
    python_requires='>=3.10, <4',

    install_requires=['generic'],
    extras_require={
        'test': ['pytest'],
    },
)
