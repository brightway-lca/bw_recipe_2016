# python-skeleton

Skeleton for Python projects that meet BONSAI guidelines.

Under development, follows the following:

* https://github.com/pyscaffold/pyscaffold
* https://docs.python-guide.org/writing/structure/
* https://github.com/modocache/pyhoe

## Getting started

The first step is to choose your library name. You should check [pypi](https://pypi.org/) to make sure your name is still available! Names should be lower case, and use underscores (`_`), not hyphens (`-`).

## License

The default license is 3-clause BSD. You need to insert your name(s) in the `LICENSE` file.

## Basic setup

Rename the directory `your_library_name` to the *exact* name of your library.

### Update `setup.py`

* Change every instance of `your_library_name` to the name of your library.
* Change `author`, `author_email`, `url`, and the PyPI [classifiers](https://pypi.org/pypi?%3Aaction=list_classifiers).

### requirements.txt

Add any python libraries which are requirements for your library to be used

## Executable

There is a skeleton executable using [docopt](http://docopt.org/) in `your_library_name/bin`.

If you want to have a command line program that you can call from a terminal, you will need to do the following:

* Rename the file `your_library_name/bin/rename_me_cli.py`
* Change the `entry_points` section in `setup.py` to match the new directory and file names

Otherwise, do the following:

* Delete the `bin` directory
* Remove `docopt` from `requirements.txt`
* Delete the `entry_points` section from `setup.py`.

## Documentation

We recommend building documentation using [sphinx](http://www.sphinx-doc.org/en/master/), and hosting documentation on [Github pages](https://pages.github.com/) or [read the docs](https://readthedocs.org/). Github pages is easier to configure, while read the docs will build automatically with each pushed commit.

To start the documentation structure, first install `sphinx` using conda or pip. Then change to the `docs` directory, and run `sphinx-quickstart`. We suggest the following **non-default** configuration values (otherwise the default is fine):

* autodoc: automatically insert docstrings from modules (y/n): `y`
* mathjax: include math, rendered in the browser by MathJax (y/n): `y`
* githubpages: create .nojekyll file to publish the document on GitHub pages (y/n): `y` if using Github pages

Note that the default format for writing code is [RestructuredText](http://docutils.sourceforge.net/rst.html), which is different than markdown (what is used in Github, and this readme). You can use [markdown with sphinx](https://www.sphinx-doc.org/en/master/usage/markdown.html).

There are other options for documenting code; the two most popular being [Asciidoctor](https://asciidoctor.org/) and [MkDocs](https://www.mkdocs.org/).

## Testing

Writing good tests is a learned art. People also have strong opinions on what makes good tests! Read some tutorials, learn about fixtures, try things out. Write unit tests, write integration tests, try TDD or BDD. Some tests are better than no tests, but no tests may be better than bad tests. 100% coverage is a journey, not a destination.

## Code quality checks

We strongly recommend using [pytest](https://docs.pytest.org/en/latest/) for testing. It is installable via conda or pip.

### pylama

[pylama](https://github.com/klen/pylama) is a collection of code quality checks which is easy to use. Just install via conda or pip, and then run `pylama <your_library_name>`. You can also run pylama on your tests with `pytest --pylama`.

## Continuous integration (CI)

The services listed here should already have permission to work with BONSAMURAIS repositories. If you are working on you own account, you will have to give permission for each service to read from GitHub. Don't worry, it is pretty simple, and there are normally good instructions.

CI testing requires that you have already written tests.

### Coveralls

Log in to https://coveralls.io/ with your GitHub account. Click on `Add Repos`, find your repository, and click on the slider button.

### Travis (Linux and MacOs)

Edit the file `.travis.yml`, and change following:

* `<add your conda dependencies here>`: Change this is a list of your conda dependencies, separated by spaces
* `<add any other dependencies not available in conda here>`: Change this to a list of dependencies not in conda, or delete this line
* `<your_library_name>`: Change as in `setup.py`

Edit the file `ci/requirements-travis.txt`, and copy everything from `requirements.txt` (but leave the testing libraries).

Log in using your GitHub account, and add the repository you want to test. Travis will now run on every pushed commit, and send coverage information to coveralls.

### Appveyor (Windows)

Edit the file `.appveyor.yml`, and change following:

* `<add your conda dependencies here>`: Change this is a list of your conda dependencies, separated by spaces
* `<add any other dependencies not available in conda here>`: Change this to a list of dependencies not in conda, or delete this line

Log in using your GitHub account, and add the repository you want to test. Then, click on settings, and change the `Custom configuration .yml file name` to `.appveyor.yml`. Appveyor will now run on every pushed commit.

## Conda `dev` package automatic uploads

This section describes how to set up `travis` to upload a development version of your library every time the CI tests run. If you don't want this, then please delete the following section from `.travis.yml`:

    if [ "$TRAVIS_BRANCH" = "master" -a "$TRAVIS_PULL_REQUEST" = "false" ]; then
        conda install conda-build anaconda-client conda-verify;
        bash ci/conda_upload.sh;
    fi

Otherwise, please do the following. This instructions are based off a [helpful gist](https://gist.github.com/zshaheen/fe76d1507839ed6fbfbccef6b9c13ed9):

* Create an account on anaconda.org.
* Create an access token. Go to `settings` > `access`, and check "Allow write access to the API site" and "Allow read access to the API site". Then give your token a name like "changethis-dev-upload" (the name doesn't matter, choose something that you will recognize in six months), and generate the token. Copy the generated string somewhere safe (DON'T share this).
* Log in to travis, click on your library, and then go to `more options` >  `settings`, and scroll down to "environment variables". Enter the variable "CONDA_UPLOAD_TOKEN" with the token you just generated.
* Change every field in `ci/meta.yaml`, `ci/macos-requirements.txt`, and `ci/conda_upload.sh` that has a `<>`.

## Upload to `pypi`

After you have set everything up, you can already upload a `0.0.1` version. You will need a [pypi account first](https://pypi.org/) ([store your account credentials](https://docs.python.org/3.7/distutils/packageindex.html#pypirc)). This is a good idea for two reasons: You will reserve your awesome project name, and you make your project more visible - outside collaborators might surprise you by just showing up! To upload to pypi, you should install [twine](https://github.com/pypa/twine) via the usual channels. Then, in your library directory (i.e. the one where `setup.py` is), run `python setup.py sdist bdist_wheel` and `twine upload dist/<my_awesome_stuff>*.*`.

## Releasing a new version

Versions should follow the [semantic versioning standard](Semantic Versioning](https://semver.org/spec/v2.0.0.html). To release a new version, you should add a description of the changes to the `CHANGELOG.md`, then change the version number in both `setup.py` and `<my_library>/__init__.py`. You can then create the distribution and upload it as before with `python setup.py` and `twine`.
