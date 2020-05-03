`develop`

[![Build Status](https://travis-ci.com/gcivil-nyu-org/spring2020-cs-gy-9223-class.svg?branch=develop&service=github)](https://travis-ci.com/gcivil-nyu-org/spring2020-cs-gy-9223-class)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/spring2020-cs-gy-9223-class/badge.svg?branch=master)](https://coveralls.io/github/gcivil-nyu-org/spring2020-cs-gy-9223-class?branch=develop&service=github)

`master`

[![Build Status](https://travis-ci.com/gcivil-nyu-org/spring2020-cs-gy-9223-class.svg?branch=master&service=github)](https://travis-ci.com/gcivil-nyu-org/spring2020-cs-gy-9223-class)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/spring2020-cs-gy-9223-class/badge.svg?branch=master)](https://coveralls.io/github/gcivil-nyu-org/spring2020-cs-gy-9223-class?branch=master&service=github)

# Requirements
- python 3.6 or above
- In case of setting up synchronization, no whitespace is allowed in the path to the project directory.

# Setup
### For Ubuntu,
1. Do
```
sudo apt install python3-dev libpq-dev
```

2. Install the follwoing dependencies:

- [PostgreSQL Setup Guide](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/PostgreSQL-Setup-Guide)
- [Geckodriver Install Instruction](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/Geckodriver---Install-instructions)
- [Grafana Setup Guide](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/Grafana-Set-Up-Guide)

3. We recommend to set up `venv`. For creating/activating venv, follow [this instruction](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

4. After you activated `venv`, iterate the following steps.

    1. Run `scripts/setup.sh`.
    2. Fix errors if any.
    3. Go to step 1.
    
### For Windows,
1. Install [python](https://www.python.org/downloads/)  and [pip](https://www.liquidweb.com/kb/install-pip-windows/). Python version should be **3.6 or later**.

2. [Create a virtual environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/). You can replace `myenv` with whatever you want to name the environment. This is to make sure that any other python related projects on your machinne are not affected by our application. This is highly recommended.

3. Install [git for windows](https://gitforwindows.org/). It's likely you'll need a bash environment to run our scripts and this is the easiest to setup for windows. Remember to [add path of installation to environment variable](https://stackoverflow.com/Questions/4492979/git-is-not-recognized-as-an-internal-or-external-command). There are better alternatives like activating [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) but it's more complicated to setup.


4. Install the follwoing dependencies:

- [PostgreSQL Setup Guide](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/PostgreSQL-Setup-Guide)
- [Geckodriver Install Instruction](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/Geckodriver---Install-instructions)
- [Grafana Setup Guide](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/Grafana-Set-Up-Guide)

## Setup Synchronization (Optional)
_Please make sure there is no whitespace in the path to the cloned repository. SymmetricDS doesn't work with a path with whitespaces._

To setup SymmetricsDs on your machine, click [here.](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/blob/master/symmetricds/README.md) In case you are on windows, please also refer to the wiki on the topic by going [here.](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/wiki/Setting-up-SymmetricDS-on-Windows) Windows support is still not streamlined but this should be enough to get you started. In case you want to help us make this better please refer below as to how you can contribute to the project.


# Run
```
python manage.py runserver
```

You should now be able to view the site at http://127.0.0.1:8000/

# Test
```
python manage.py test
```

# HOWTO Contribute to this repo

Refer to our contributing guidelines [here.](https://github.com/gcivil-nyu-org/spring2020-cs-gy-9223-class/blob/master/CONTRIBUTING.md)

# Fix issues
Running into issues with modules not find? Did `requirements.txt` update from your last `git pull` command? Run `pip install -r requirements.txt` to install missing modules.

Are you missing staticfiles when trying to run or test locally? Run `python manage.py collectstatic` to regenerate them.
