from setuptools import setup, find_packages

setup(
    name='infra-awscdk-devops-packages',
    version='0.1.61',
    description='Python package for AWS CDK infrastructure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/<your-company>/infra-awscdk-devops-packages.git',
    packages=find_packages(exclude=["tests", "tests.*", "stacks", "stacks.*", "dist", "dist.*", "*.egg-info/"]),
    include_package_data=True,
    keywords='infra awscdk devops packages',
    zip_safe=True,
    install_requires=[
        'aws-cdk-lib==2.175.1',
        'constructs>=10.0.0,<11.0.0',
        'pyyaml==6.0.1',
        'aws-cdk.lambda-layer-kubectl-v31==2.0.0'
    ],
    classifiers=[
        "Requires-Python: >=3.8,<4.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='>=3.8,<4.0'
)