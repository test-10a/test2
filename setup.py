from setuptools import setup, find_packages

setup(
    name='resume-analysis-tool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pycryptodome', 
        'security-package==1.0'  
    ],
    entry_points={
        'console_scripts': [
            'analyze-resume=resume_analysis.analyzer:main',
        ],
    },
)
