#!/bin/bash

RED='\033[0;31m'          # Red
GREEN='\033[0;32m'        # Green
RESET='\033[0m'       # Text Reset
function __system {
    echo -e $GREEN$*$RESET
}
function __error {
    echo -e $RED$*$RESET
}
function __success {
    echo -e $GREEN"[OK] "$*$RESET
}
function __assert_exist {
    if command -v "$1" > /dev/null; then
        __success $1
    else
        __error "[ERR] "$1
        echo ""
        __system "Please install "$1" first"
        __system $2
        exit 1
    fi
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR/.."

if [[ -z $VIRTUAL_ENV ]]; then
  printf $RED
  read -n 1 -p "You haven't activated virtualenv. Do you want to proceed? (yN)? " yn
  echo -e $RESET
  case $yn in
        y ) ;;
        * ) exit 0 ;;
  esac
else
  __success "virtualenv activated"
fi

__assert_exist psql "https://github.com/mercury-telemetry/mercury-telemetry/wiki/PostgreSQL-Setup-Guide#install"

ENV_SAMPLE=$SCRIPT_DIR/env.sample
if [[ ! -f ".env" ]]; then
  cp "$ENV_SAMPLE" .env
  __success "Copy .env at the project root"
elif diff .env scripts/env.sample > /dev/null; then
  __success "Skip copying .env"
else
    printf $GREEN
    read -n 1 -p "You already have '.env'. Do you want to overwrite it? (yN)" yn
    echo -e $RESET
    case $yn in
          y ) cp "$ENV_SAMPLE" .env ;;
          q ) exit 0 ;;
    esac
fi

# Install wheel first to avoid issue 
# https://stackoverflow.com/questions/34819221/why-is-python-setup-py-saying-invalid-command-bdist-wheel-on-travis-ci
pip3 install wheel

echo ""
__system "Running pip3 install -r requirements.txt..."
pip3 install -r requirements.txt || exit 1
__success "pip install -r requirements.txt"

echo ""
printf $GREEN
read -n 1 -p "Do you also want to install test requirements? (black, flake8, coveralls, etc.) (Yn)" yn
echo -e $RESET
case $yn in
  n ) ;;
  * )
    __assert_exist geckodriver "https://github.com/mercury-telemetry/mercury-telemetry/wiki/Geckodriver---Install-instructions"
    pip3 install -r test-requirements.txt || exit 1
    __success "pip install -r test-requirements.txt"
    ;;
esac

source $SCRIPT_DIR/../.env
[[ -z $DB_USER ]] && DB_USER="postgres"
[[ -z $DB_PASSWORD ]] && DB_PASSWORD=""
[[ -z $DB_HOST ]] && DB_HOST="localhost"
[[ -z $DB_PORT ]] && DB_PORT="5432"

echo ""
__system "Checking postgres connection..."
if ! psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT -c "" ; then
  __error "[ERR] No postgres running on postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT"
  echo ""
  __system "Make sure you have PostgreSQL installed and running."
  __system "https://github.com/mercury-telemetry/mercury-telemetry/wiki/PostgreSQL-Setup-Guide"
  exit 1
fi

__success "postgres connection"

if ! psql postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT -c "CREATE DATABASE mercury;" 2> /dev/null; then # if it already exists, an error occurs. ignore it
  __system "Skip creating mercury database"
fi

__success "mercury database"

echo ""
__system "Creating migration files and running database migrations..."
python manage.py makemigrations || exit 1
python manage.py migrate || exit 1
__success "django migration"

echo ""
__system "Collecting static files..."
python manage.py collectstatic --noinput || exit 1
__success "python manage.py collectstatic --noinput"

echo ""
__system "Done!"
__system "Run 'python manage.py runserver' to start the Django webserver."
