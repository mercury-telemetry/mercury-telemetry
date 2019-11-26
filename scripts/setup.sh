#!/usr/local/bin/bash

if [[ ! -d ".git" ]]; then
  echo "You must run this script from the top-level (root) directory of this repository."
  exit 1
fi
echo "===> Setting up repo..."
read -p "About to install Python requirements. Press Ctrl+C if you need to enter a virtualenv first, or press return to continue."
echo "DATABASE_URL=sqlite:///db.sqlite3" > .env
echo "===> Running pip3 install -r requirements.txt"
pip3 install -r requirements.txt
echo "===> Creating migration files and running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Run 'python manage.py runserver' to start the Django webserver."