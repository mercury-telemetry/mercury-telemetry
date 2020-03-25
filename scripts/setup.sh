#!/bin/bash

if [[ ! -d ".git" ]]; then
  echo "You must run this script from the top-level (root) directory of this repository."
  exit 1
fi
echo "===> Setting up repo..."
read -p "About to install Python requirements. Press Ctrl+C if you need to enter a virtualenv first, or press return to continue."

ENV_SAMPLE=scripts/env.sample
if [[ ! -f ".env" ]]; then
  cp $ENV_SAMPLE .env
elif ! diff .env scripts/env.sample > /dev/null; then
  echo "You already have '.env'. Do you want to overwrite it?"
  select yn in "Yes" "No" "See diff"; do
        case $yn in
              Yes ) cp $ENV_SAMPLE .env; break;;
              No ) break;;
              "See diff" ) diff .env $ENV_SAMPLE;;
              q ) break;;
        esac
  done
fi

echo "===> Running pip3 install -r requirements.txt"
pip3 install -r requirements.txt
echo "===> Creating migration files and running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Run 'python manage.py runserver' to start the Django webserver."
