`master`

[![Build Status](https://travis-ci.com/mercury-telemetry/mercury-telemetry.svg?branch=master)](https://travis-ci.com/mercury-telemetry/mercury-telemetry)
[![Coverage Status](https://coveralls.io/repos/github/mercury-telemetry/mercury-telemetry/badge.svg?branch=master)](https://coveralls.io/github/mercury-telemetry/mercury-telemetry?branch=master)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)

# Mercury
Mercury is a telemetry system that provides software and instructions that will allow you to: 
- attach telemetry sensors to a Raspberry Pi
- record and transmit sensor data via WiFi and/or radio to a data collection endpoint 
- visualize the data live or retroactively from the Mercury web application
- export the data and analyze it in other ways

Mercury consists of the following components: 
### 1. Mercury Telemetry Hardware 
- Instructions, firmware, and software for setting up a Raspberry Pi to collect/transmit data from your sensors and relay it to a data collection endpoint (the Mercury web app).

### 2. Mercury Web App
- **If you are only interested in collecting data**, because you are planning to visualize the data using other methods, the web app can act as a simple endpoint, retrieving and processing data from the sensors and storing it in a local or cloud-hosted Postgres database. 
- **If you are also interested in visualizing your data**, we provide an integration with the visualization tool, `Grafana`, which will allow you to create a custom panel for each of your sensors and view your telemetry data live from a Grafana dashboard (see `Fig. 1` below). 
- The Mercury web application can be either run locally on your machine or deployed on a web-hosting service like Heroku.

### 3. Database Synchronization
- If you are transmitting data in a location with intermittent radio vs. WiFi transmission capabilities, and would like to have the option to transmit via both radio and WiFi, we provide a guide for you to set up database synchronization between the database receiving the radio transmissions and the database receiving the WiFi transmissions.

![fig 1](docs/imgs/grafana_dashboard.png)
**Fig 1**: Grafana dashboard with 3 sensor panels: GPS, temperature, and speed.

# Installation Overview
- [Install Mercury](#install-mercury)
    - [Local Set-Up](#local-set-up)
    - [Cloud Deployment On Heroku](#cloud-deployment-on-heroku)
- [Install Grafana](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_grafana.md#a-install-grafana)
	- [Set-up Database Synchronization](#setup-synchronization)

# Documentation
- Mercury
    - We recommend that you start by [installing Grafana](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_grafana.md#a-install-grafana), then look at our [walkthrough](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_grafana.md#6-a-walkthrough-example), which will give you an idea of the sequence of steps needed to visualize sensor data live in Grafana.
    - [Configure Grafana](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_grafana.md): A guide for installing Grafana and connecting a Grafana host to your Mercury deployment. Once Grafana is hooked up to Mercury, the two will remain in sync, and all of the sensors you add/update/remove in Mercury will be updated in Grafana.
    - [Configure Sensors](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_sensors.md): A guide for creating and managing your sensors in Mercury. These sensors will be used to generate Sensor Panels in Grafana.  
    - [Manage Events](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/docs/configure_events.md): A guide for creating, managing, and exporting data from events. Mercury organizes sensor data collection into Events, so whenever you have a new recording session, create a new Event. All incoming sensor data transmissions will be stored under the **Active Event**, which can be toggled through the Mercury web app. This will allow you to keep your measurement data organized. Each Event will have an Event Dashboard in Grafana, which will display only the data recorded for that Event. 
    
## Local Setup
### For Unix-like OS
1. Install python and psycopg2 dependencies
```
## Ubuntu/Debian
sudo apt install python3-dev libpq-dev

## RPM-based Linux
# Now we only tested on Fedora 31 successfully, 
# but there should be very little differences on other RPM-based Linux systems. 
# If you can test on centOS/RedHat/OpenSuse and other versions of Fedora, please give us some feedback.
# Thanks for your help!
#
# dnf is yum's successor. In Fedora 31/32, you can still use yum as package manager
sudo dnf install python-devel libpq-devel

## macOS
# Detailed step is coming soon
# If you receive errors when installing psycopg2, try using:
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
```

2. Install the following dependencies:

    - [PostgreSQL Setup Guide](https://github.com/mercury-telemetry/mercury-telemetry/wiki/PostgreSQL-Setup-Guide)
    - [Geckodriver Install Instruction](https://github.com/mercury-telemetry/mercury-telemetry/wiki/Geckodriver-Install-instructions)
    - [Grafana Setup Guide](https://github.com/mercury-telemetry/mercury-telemetry/wiki/Grafana-Set-Up-Guide)

3. We recommend to set up `venv`. For creating/activating venv, follow [this instruction](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

4. After you activated `venv`, iterate the following steps.

    1. Run `scripts/setup.sh`.
    2. Fix errors if any.
    3. Go to step 1.
    
### For Windows
1. Install [python](https://www.python.org/downloads/)  and [pip](https://www.liquidweb.com/kb/install-pip-windows/). Python version should be **3.6 or later**. Make sure that python installation is in your PATH environment variable.

2. [Create a virtual environment](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/). You can replace `myenv` with whatever you want to name the environment. This is to make sure that any other python related projects on your machine are not affected by our application. This is highly recommended.

3. Install [git for windows](https://gitforwindows.org/). It's likely you'll need a bash environment to run our scripts and this is the easiest to setup for windows. Remember to [add path of installation to PATH environment variable](https://stackoverflow.com/Questions/4492979/git-is-not-recognized-as-an-internal-or-external-command). There are better alternatives like activating [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) but it's more complicated to setup.

4. Install the following dependencies:
    - [PostgreSQL Setup Guide](https://github.com/mercury-telemetry/mercury-telemetry/wiki/PostgreSQL-Setup-Guide)
    - [Geckodriver Install Instruction](https://github.com/mercury-telemetry/mercury-telemetry/wiki/Geckodriver---Install-instructions)
    
5. Since our scripts use linux commands for automation, you will need to install them on your windows machine. It's quite easy to do so. Install [curl for windows](https://curl.haxx.se/windows/), choose 32 or 64 bit according to your machine. Extract downloaded zip file to a folder named `curl`, wherever you wish to have it installed. Install [zip.exe and unzip.exe](http://stahlworks.com/dev/index.php?tool=zipunzip). Place these 2 in your curl folder. **Add the path of your curl folder to windows PATH environment variable**. Lastly, download and install [coreutils for windows](http://gnuwin32.sourceforge.net/downlinks/coreutils.php).  

6. Make a local copy of our project. You can download it as zip or clone our repo.

7. Using command prompt, `cd` into `scripts` folder of our project repository then simply type `setup.sh`. Git bash should automatically open (assuming it was added to PATH) and should automatically install requirements as well as ask if you need to install test requirements. Say yes. If you get some errors, fix them.

8. Now run `python manage.py runserver`. Go to http://127.0.0.1:8000/ in your browser. You should be able to access our project.

## Cloud Deployment On Heroku
1. Install Heroku CLI
   1. Instructions can be found here: https://devcenter.heroku.com/articles/heroku-cli
       * For macOS: `brew tap heroku/brew && brew install heroku`
       * For Ubuntu/Debian `curl https://cli-assets.heroku.com/install-ubuntu.sh | sh`
       * For Arch Linux `yay -S heroku-cli`
       * For Windows: Use this link address to install 64bit installer https://cli-assets.heroku.com/heroku-x64.exe OR Use this link address to install 32 bit installer https://cli-assets.heroku.com/heroku-x86.exe
   2.  Verify your installation: Running `heroku --version`, output should be like `heroku/x.y.z`

2. Heroku Deployment
   1. Create an account in [Heroku.](https://signup.heroku.com/) 
   2. Login your Heroku account in terminal by using `heroku login`
   3. Go to http://dashboard.heroku.com/new-app to create a new Heroku instance
   4. Go to new created instance page, then choose "Resources", in the add-ons search postgres, choose Heroku-Postgres, then click "Provision" to add it.
   5. Add a remote to local project, using comand `heroku git :remote -a <heroku-project-name>` .
   6. Deploy to Heroku `git push heroku master`
3. Visit remote site: \<heroku-project-name\>.herokuapp.com

## Setup Synchronization (Optional)

_Please make sure there is no whitespace in the path to the cloned repository. SymmetricDS doesn't work with a path with whitespaces._

To setup SymmetricDS on your machine, click [here.](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/symmetricds/README.md) In case you are on windows, please also refer to the wiki on the topic by going [here.](https://github.com/mercury-telemetry/mercury-telemetry/wiki/Setting-up-SymmetricDS-on-Windows) Windows support is not streamlined and is very error prone but this should be enough to get you started. In case you want to help us make this better please refer below as to how you can contribute to the project.

# Run
```
python manage.py runserver
```

You should now be able to view the site at http://127.0.0.1:8000/

# Test
```
python manage.py test
```

# How to contribute to this repo

Refer to our contributing guidelines [here.](https://github.com/mercury-telemetry/mercury-telemetry/blob/master/CONTRIBUTING.md)

# Fix issues
Running into issues with modules not find? Did `requirements.txt` update from your last `git pull` command? Run `pip install -r requirements.txt` to install missing modules.

Are you missing staticfiles when trying to run or test locally? Run `python manage.py collectstatic` to regenerate them.

# License

Copyright (c) Mercury Telemetry. All rights reserved.

Licensed under the [MIT](LICENSE.txt) license.
