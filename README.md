# Team Project repo
Heroku Production URI: [https://nyu-mercury.herokuapp.com](https://nyu-mercury.herokuapp.com)

Heroku Dashboard: [https://dashboard.heroku.com/apps/nyu-mercury](https://dashboard.heroku.com/apps/nyu-mercury)
# HOWTO Contribute to this repo

N.B.: `<something>` means you need to change the `something` text within the angle brackets (and do not include the include brackets in your command).
1) Make a feature branch
`git checkout -b <new_branch_name>`
2) Make your changes
3) Use `git add <filename> ...` to add files you changed or more conveniently, `git add -A`.
4) Commit your changes with `git commit -m "<message_of_what_this_commit_does>"`.
5) Push your branch to the origin fork with `git push origin <new_branch_name>` of the branch you made locally.
6) Visit [our repo](https://github.com/gcivil-nyu-org/fall2019-cs-gy-6063-team-moonsurvivors/pulls) to create a Pull Request or use the link that the `git` command printed for you.
7) Add someone on the team as a review or share your URL to the Slack channel.

# HOWTO Push to Heroku
Assuming you have setup a Git remote called `heroku`, you can run `git push heroku <local_branch>:master` if you _really_ need to test your local changes on the Heroku app.