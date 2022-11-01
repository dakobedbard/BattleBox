import setuptools

setuptools.setup(
    name='battlebox_logic',
    version='1.0.0',
    author='Marcel Vonlanthen',
    author_email='vonlanth@amazon.com',
    description='test library 1',
    packages=setuptools.find_packages(),
    install_requires=[
        "pynamodb"
    ]
)