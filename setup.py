import setuptools

version = "0.0.1"


setuptools.setup(
    name="puppetdb_exporter",
    version=version,
    description="Prometheus puppetdb exporter",
    author="Florian Chardin",
    author_email="othalla.lf@gmail.com",
    url="https://github.com/othalla/puppetdb_exporter",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(exclude=['tests*']),
    package_data={},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
    install_requires=[
        "pypuppetdb==0.3.3",
        "prometheus-client==0.5.0",
    ],
    extras_require={},
)
