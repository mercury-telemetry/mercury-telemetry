This file contains information regarding how to contribute to this project. To be updated.

# Contributing guidelines
Overview will be added

## Code of Conduct
Link to code of conduct

## Contributor Workflow
1. Make a feature branch `git checkout -b <new_branch_name>`. Then, make your changes
2. Ensure that you include tests that exercise not only your feature, but also any other code that might be impacted. This is very important.
3. Check you are using consistent style by running `scripts/check.sh` and make any recommended changes (such as running black to re-format). Then run your tests with `python manage.py test` and fix errors. 
4. Add files you changed using `git add -A`. Then commit your changes with `git commit -m "<what_this_commit_does>"`.
Please keep in mind that your commits should be [atomic](https://en.wikipedia.org/wiki/Atomic_commit#Atomic_commit_convention) and the diffs should be easy to read/understand. This will help in improving the maintainability of our project.
5. Push your branch to the origin fork with `git push origin <new_branch_name>` of the branch you made locally.

## Pull request process and guidelines
1. Check that there are no conflicts and your request passes Travis build as well as coveralls requirements. Check the log if any of the 3 checks fail.
2. Give the description of the issue that you want to resolve in the pull request message. Include the relevant issue number if applicable.
3. Wait for the maintainers to review your pull request and do the changes if requested.

Guidelines will be added soon
## Asking Questions
Details will be added soon

## Reporting Issues
Details will be added soon



