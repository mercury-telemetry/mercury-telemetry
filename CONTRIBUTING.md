# Contributing guidelines
This document contains everything you need in order to contribute to our project. We welcome everyone to collaborate and help us improve our product. In addition to all the information present in this document, make sure to take a look at our [Wiki.](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki)

## Code of Conduct
You can access our code of conduct [here](). 


## Reporting Issues
This section guides you through reporting an issue. Following these guidelines will help maintainers to understand your issue and in case you are reporting a bug, reproduce the behavior.

#### For reporting bugs:
* Check the [Wiki.](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki) and make sure you followed all the steps to install and configure our application accurately. 

* Search to see if the problem has already been reported. If it has and is still open, add a comment to the existing issue instead of opening a new one.

* Create an issue on master repository and provide the following information by filling in the template.

  1. Use a clear and descriptive title for the issue to identify the problem.
  2. If reporting as bug, describe the exact steps which reproduce the problem in as many details as possible.
  3. If reporting as bug, describe the behavior you observed after following the steps and point out what exactly is the problem with that behavior. Include screenshots if possible.

 *Note: If you find a closed issue that is same as your issue, and you have followed the setup steps accurately, open a new issue and include a link to the original issue in the body of your new one.*

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

#### Guidelines for making a PR
* Keep each PR focused. While it might seem convenient, do not combine several unrelated fixes together. It can cause confusion to the maintainers. Feel free to create new branches to keep each PR focused.

* If your PR is a bug fix, please also include a test that demonstrates the problem, or modifies an existing test that wasn't catching that problem already. Of course, it's not a requirement, so proceed anyway if you can't figure out how to write a test, but do try. Without having a test your fix could be lost down the road. By supplying a test, you're ensuring that your projects won't break in the future.

* Do this for PRs that implement new features as well. Without having a test case validating this new feature, it'd be very easy for that new feature to break in the future. A test case ensures that the feature will not break. 

* In case you're submitting a PR for a UI related issue, it is recommended (This is not a must but a ***very*** nice to have) if you add a screenshot of your change or a link to a deployment (heroku is fine) where it can be tested out along with your PR. It will make the review process a lot faster. 

* Please use the appropriate tags for your PR. 

## Asking Questions
Details will be added soon




