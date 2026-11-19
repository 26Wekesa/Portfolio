# Chris Tech Solutions portfolio

This site is served by Django. The existing `.html` page URLs and `assets/`
directory are retained. Contact submissions are stored in SQLite locally and
PostgreSQL in production, emailed to the configured recipient, and available in
Django admin.

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

## Recommended hosting: Render

[Render](https://render.com/docs/deploy-django) is a suitable first deployment
target because it can run this Django application and provide a managed
PostgreSQL database. Netlify alone serves static sites and does not run Django
or its admin.

Create a Render PostgreSQL database and set the web service's `DATABASE_URL` to
its internal connection URL. In the web service environment, also set
`DJANGO_SECRET_KEY` to a strong secret, `DJANGO_DEBUG=0`,
`DJANGO_ALLOWED_HOSTS` to the service hostname, and the SMTP settings above.
When the service is available, run `python manage.py migrate` and
`python manage.py createsuperuser` in its shell. The admin will then be at
`https://<your-service-hostname>/admin/`.

Production mode requires `DATABASE_URL` to point to PostgreSQL; it will not
silently fall back to SQLite. Local development continues to use SQLite unless
`DATABASE_URL` is set. WhiteNoise serves compressed static assets in production.
Set the Render build command to install requirements and run
`python manage.py collectstatic --no-input`; the service start command and
remaining deployment settings still need to be configured.
