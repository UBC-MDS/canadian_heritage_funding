# Contributing to the Canadian Heritage Funding  
This outlines how to propose a change to the Canadian Heritage Funding project.

>We welcome all contributions to this project! If you notice a bug, or have a feature request, please open up an issue here. If you’d like to contribute a feature or bug fix, you can fork our repo and submit a pull request. We will review pull requests within 7 days. All contributors must abide by our code of conduct.

## Fixing typos  
Small typos or grammatical errors in documentation may be edited directly using the GitHub web interface, so long as the changes are made in the source file.

## Prerequisites  
For larger scale contribution, it is necessary to file an issue and make sure someone from the core team agrees that the recommended fix is a problem before you make a substantial pull request. If you've found a bug, create an associated issue and illustrate the bug with a minimal reproducible example.

## Pull request process  
We recommend that you create a Git branch for each pull request (PR).
New code should follow the [Numpy](https://numpydoc.readthedocs.io/en/latest/format.html) style guide or [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.

>### Creating a Branch  
>Once your local environment is up-to-date, you can create a new git branch which will contain your contribution:  
>```$ git checkout -b <branch-name>```

>With this branch checked-out, make the desired changes to the package. Note that our code uses the black code formatter, which you can apply to your modifications by installing and running black on the local directory:
>```
$ pip install black
$ black .

>When you are happy with your changes, you can commit them to your branch by running
>```
$ git add <modified-file>
$ git commit -m "Some descriptive message about your change"

## Code of Conduct  
Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## Attribution  
These contributing guidelines were adapted from the [Altair](https://github.com/altair-viz/altair/blob/master/CONTRIBUTING.md) contributing guidelines.