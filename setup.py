from setuptools import setup, find_packages

setup(
    name='entyty',
    version='0.0.1',
    description='A Python library for creating and managing entities.',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/entyty',
    packages=find_packages(),
    install_requires=['pyglet'],
    python_requires='>=3.7',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Games/Entertainment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='entity game development grid'
)