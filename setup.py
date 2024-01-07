from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    description = file.read()

setup(
    name='iqoptionbot',
    version='0.1.0',
    description='IQ Option Bot for operating M5 retracement.',
    long_description=description,
    long_description_content_type='text/markdown',
    keywords=['technical analysis', 'ta', 'trading', 'bot', 'iqoption'],
    url='https://github.com/EsauM10/iqoptionbot',
    author='Esaú Mascarenhas',
    author_email='esaumasc@gmail.com',
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires = [
        'Flask',
        'Flask-SocketIO',
        'tradingbot @ git+https://github.com/EsauM10/tradingbot.git',
    ],
    entry_points={
        'console_scripts': [
            'iqoptionbot = iqoptionbot.scripts:main',
        ]
    },
    include_package_data=True,
    zip_safe=False
)