#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create a superuser non-interactively (only if not exists)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')" | python manage.py shell

# Setup site information
python manage.py setup_site

# Update requirements.txt
pip freeze > requirements.txt

# Run the development server
echo "Server starting at http://localhost:8000/"
echo "Admin credentials: email=admin@example.com, password=adminpassword"
echo "Ctrl+C to stop the server"
python manage.py runserver