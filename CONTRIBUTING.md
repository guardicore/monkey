# Hi there 🐵

Thanks for your interest in making the Monkey -- and therefore, your network -- a better place!

Are you about to report a bug? Sorry to hear it. Here's our 
[Issue tracker](https://github.com/guardicore/monkey/issues).
Please try to be as specific as you can about your problem; try to include steps
to reproduce. While we'll try to help anyway, focusing us will help us help you faster.

If you want to contribute new code or fix bugs, please read the following sections. You can also contact us (the 
maintainers of this project) at our [Slack channel](https://join.slack.com/t/infectionmonkey/shared_invite/enQtNDU5MjAxMjg1MjU1LTM2ZTg0ZDlmNWNlZjQ5NDI5NTM1NWJlYTRlMGIwY2VmZGMxZDlhMTE2OTYwYmZhZjM1MGZhZjA2ZjI4MzA1NDk). 

## Submitting Issues
* **Do** write a detailed description of your bug and use a descriptive title.
* **Do** include reproduction steps, stack traces, and anything else that might help us verify and fix your bug.

You can look at [this issue](https://github.com/guardicore/monkey/issues/430) for an example. 

## Submitting Code

The following is a *short* list of recommendations. PRs that don't match these criteria won't be closed but it'll be harder to merge the changes into the code.

* **Do** stick to [PEP8](https://www.python.org/dev/peps/pep-0008/).
* **Do** target your pull request to the **develop branch**. 
* **Do** specify a descriptive title to make searching for your pull request easier.
* **Do** list verification steps so your code is testable.
* **Don't** leave your pull request description blank.
* **Do** license your code as GPLv3.

Also, please submit PRs to the `develop` branch.

#### Unit Tests
**Do** add unit tests if you think it fits. We place our unit tests in the same folder as the code, with the same 
filename, followed by the _test suffix. So for example: `somefile.py` will be tested by `somefile_test.py`.

Please try to read some of the existing unit testing code, so you can see some examples.

#### Branches Naming Scheme
**Do** name your branches in accordance with GitFlow. The format is `ISSUE_#/BRANCH_NAME`; For example, 
`400/zero-trust-mvp` or `232/improvment/hide-linux-on-cred-maps`.

#### Continuous Integration
We use [TravisCI](https://travis-ci.com/guardicore/monkey) for automatically checking the correctness and quality of submitted 
pull requests. If your build fails, it might be because of one of the following reasons: 
* Syntax errors.  
* Failing Unit Tests.
* Too many linter warnings.

In any of these cases, you can look for the cause of the failure in the _job log_ in your TravisCI build.

#### Thank you for reading this before opening an issue or a PR, you're already doing good!
