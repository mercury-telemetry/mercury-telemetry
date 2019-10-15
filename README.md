# Team Project repo

# HOWTO Contribute to this repo

N.B.: `<something>` means you need to change the `something` text within the angle brackets.
1) Make a feature branch
`git checkout -b <new_branch_name>`
2) Make your changes
3) Use `git add <filename> ...` to add files you changed or more conveniently, `git add -A`.
4) Commit your changes with `git commit -m "<message_of_what_this_commit_does>"`.
5) Push your branch to the origin fork with `git push origin <new_branch_name>` of the branch you made locally.
6) Visit [our repo](https://github.com/gcivil-nyu-org/fall2019-cs-gy-6063-team-moonsurvivors/pulls) to create a Pull Request or use the link that the `git` command printed for you.
7) Add someone on the team as a review or share your URL to the Slack channel.

# HOWTO Run the app locally
python manage.py runserver

# HOWTO prepare to push to Heroku
1) heroku login
3) heroku git:remote -a nyu-mercury
Repo now has a remote called "heroku" that can be pushed to using "git push heroku"

# HOWTO configure Django app for deployment
Add the following lines to settings.py
    import django_heroku
    django_heroku.settings(locals())
Create a Procfile containing the following line
    web: gunicorn <project-name>.wsgi
Create a requirements.txt containing the following lines
    gunicorn
    django-heroku