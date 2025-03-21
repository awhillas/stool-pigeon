# Stool Pigeon

A Django-based app for tracking your stool health with easy logging and monitoring.

## Features

- Track stool types based on the Bristol Stool Chart
- One-click recording of stool events
- View recent stool history
- Secure authentication with Google OAuth
- Mobile-friendly Bootstrap interface with Dark Mode
- HTMX for seamless front-end interactions without page reloads
- No email verification required

## Setup

### Prerequisites

- Python 3.13
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stool-pigeon.git
cd stool-pigeon
```

2. Create and activate a virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

### Google OAuth Setup (For Production)

1. Visit the [Google Developer Console](https://console.developers.google.com/)
2. Create a new project
3. Enable the Google+ API
4. Create OAuth credentials
5. Add your domain to the authorized domains
6. Update the OAuth credentials in the Django admin interface

## Development

Run the development server:

```bash
./run_dev.sh
```

This script will:
- Activate the virtual environment
- Run migrations
- Create a default superuser (if not exists)
- Setup the site configuration
- Start the development server

Visit http://localhost:8000/ to access the application.

Admin interface is available at http://localhost:8000/admin/
Default admin credentials:
- Email: admin@example.com
- Password: adminpassword

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.