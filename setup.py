from setuptools import find_packages, setup

setup(
    name="sops-pre-commit",
    description="Check for unencrypted Kubernetes secrets in manifest files",
    url="https://github.com/nicholasklem/sops-pre-commit",
    version="3.0.0",
    author="Devin Buhl, nicholasklem",
    platforms="linux",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages("."),
    install_requires=["pyyaml>=5.1"],
    entry_points={
        "console_scripts": [
            "forbid_secrets = hooks.forbid_secrets:main",
        ],
    },
)
