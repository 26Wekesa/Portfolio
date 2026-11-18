# Chris Tech Solutions portfolio

This site is served by Django. The existing `.html` page URLs and `assets/`
directory are retained. Contact submissions are stored in SQLite, emailed to
the configured recipient, and available in Django admin.

## Run locally

```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
```

Configure SMTP in the same PowerShell session before starting the server:

```powershell
$env:EMAIL_HOST = "smtp.example.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "1"
$env:EMAIL_HOST_USER = "your-smtp-user"
$env:EMAIL_HOST_PASSWORD = "your-smtp-password"
$env:DEFAULT_FROM_EMAIL = "your-sender@example.com"
$env:CONTACT_RECIPIENT = "wekesachristopher@gmail.com"
py manage.py runserver
```

Use an SMTP app password where your provider requires one, and keep credentials
in environment variables or your hosting provider's secret manager. Do not
commit them to source control. The recipient defaults to the email address
shown on the portfolio and can be overridden with `CONTACT_RECIPIENT`.

Open `http://127.0.0.1:8000/`. Contact messages are available at
`http://127.0.0.1:8000/admin/` after signing in. If SMTP is unavailable, the
message remains saved and the form reports that email notification failed.

Before deployment, set `DJANGO_SECRET_KEY` to a secure secret,
`DJANGO_DEBUG=0`, and `DJANGO_ALLOWED_HOSTS` to the site's hostnames. Run
`py manage.py collectstatic` and configure the production web server to serve
the collected static files from `staticfiles/`, along with the SMTP environment
variables above.
