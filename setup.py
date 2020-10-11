from setuptools import setup, find_packages

setup(
    name='theme_switcher',
    version='0.1',
    author='Neeraj Nishant',
    license='GPLv3',
    install_requires=[
        'PyGObject',
        'pydbus'
    ],
    description='An application to switch between light/dark themes based on various conditions',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Consumers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only'
    ],
    data_files=[
        (
            'share/theme-switcher/',
            [
                'data/current_theme',
                'data/initial_setup',
                'data/theme-switcher.desktop',
                'data/themes.json',
                'data/config.json'
            ]
        ),
        (
            'bin/',
            [
                'data/theme_manager'
            ]
        )
    ],
    python_requires='>=3.5',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'theme_switcher=theme_switcher:main'
        ]
    }
)
