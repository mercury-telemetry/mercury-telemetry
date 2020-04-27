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

### Guidelines for PR
* Keep each PR focused. While it might seem convenient, do not combine several unrelated fixes together. It can cause confusion to the maintainers. Feel free to create new branches to keep each PR focused.

* If your PR is a bug fix, please also include a test that demonstrates the problem, or modifies an existing test that wasn't catching that problem already. Of course, it's not a requirement, so proceed anyway if you can't figure out how to write a test, but do try. Without having a test your fix could be lost down the road. By supplying a test, you're ensuring that your projects won't break in the future.

* Do this for PRs that implement new features as well. Without having a test case validating this new feature, it'd be very easy for that new feature to break in the future. A test case ensures that the feature will not break. 

* In case you're submitting a PR for a UI related issue, it is recommended (This is not a must but a ***very*** nice to have) if you add a screenshot of your change or a link to a deployment (heroku is fine) where it can be tested out along with your PR. It will make the review process a lot faster. 

* Please use the appropriate tags for your PR. 

## Asking Questions
Details will be added soon

## Reporting Issues
Details will be added soon



