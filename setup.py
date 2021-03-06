import setuptools

pkg_name = "labbox_ephys"

setuptools.setup(
    name=pkg_name,
    version="0.1.0",
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    description="Python package for labbox_ephys",
    packages=setuptools.find_packages(),
    scripts=[
        'bin/le-processing-daemon'
    ],
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
