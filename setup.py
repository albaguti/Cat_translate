from setuptools import setup, find_packages

setup(
    name='cattranslate',
    version='1.0.0',
    description='App per traduir automàticament paraules.',
    author='Alba Gutierrez Pedemonte',
    author_email='albaguti@gmal.com',
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "translate"
    ],
)
