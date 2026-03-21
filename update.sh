#!/bin/bash
# update.sh - Use this for pushing code changes
set -e

PROJECT_DIR="/home/ajhope/foundationsite"
PROJECT_NAME="foundationsite"

cd $PROJECT_DIR

# 1. Pull latest code (if using git)
# git pull origin main

# 2. Update dependencies and migrate
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# 3. Restart services
sudo systemctl restart gunicorn_${PROJECT_NAME}
# Only restart Nginx if you changed the nginx config
# sudo systemctl restart nginx

echo "Update complete!"