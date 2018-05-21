from setuptools import setup

setup(
    name="hetznercloud",
    packages=["hetznercloud"],
    version="1.0.3",
    description="Hetzner Cloud SDK",
    author="Liam Symonds",
    author_email="liam@ls-software.uk",
    url="https://github.com/elsyms/hetznercloud-py",
    keywords=["hetzner", "hetznercloud", "hetzner cloud api", "hetzner sdk", "hetzner api"],
    classifiers=[],
    install_requires=["requests==2.18.4"]
)