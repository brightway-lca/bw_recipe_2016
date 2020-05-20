from setuptools import setup


v_temp = {}
with open("bw_recipe_2016/version.py") as fp:
    exec(fp.read(), v_temp)
version = ".".join((str(x) for x in v_temp["version"]))


setup(
    name="bw_recipe_2016",
    version=version,
    packages=[
        "bw_recipe_2016",
        "bw_recipe_2016.strategies",
        "bw_recipe_2016.categories",
    ],
    author="Chris Mutel",
    author_email="cmutel@gmail.com",
    license="BSD 3-clause",
    package_data={"bw_recipe_2016": ["data/*.xlsx", "data/*.json"]},
    install_requires=[
        "bw2io",
        "bw2data",
        "requests",
    ],
    url="https://github.com/brightway-lca/bw_recipe_2016",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    description="Import ReCiPe 2016 into Brightway2",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
