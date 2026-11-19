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

## Render development deployment

The root [`render.yaml`](./render.yaml) defines a free Render web service and
free Render PostgreSQL database in Frankfurt. To deploy it, push the repository
to GitHub, then in the Render Dashboard choose **New > Blueprint**, connect this
repository and the `main` branch, review the resources, and choose **Deploy
Blueprint**. This file does not create resources until you deploy the Blueprint.

Render generates `DJANGO_SECRET_KEY` and the initial admin password. The
Blueprint applies database migrations at service startup and creates the
`portfolio-admin` superuser after the first successful deploy. Retrieve and
store the generated `DJANGO_SUPERUSER_PASSWORD` securely in the Render
Dashboard; the admin URL will be `https://<your-service-hostname>/admin/`.

**This free configuration is only suitable for a development preview, not
reliable production hosting:**

- Free web services sleep after 15 minutes without traffic, and waking can take
  about a minute. Their filesystem is temporary and they have no shell access.
- Free services count against Render's included usage limits. Monitor bandwidth
  and build usage in the Render Dashboard; overages can be billed if billing is
  enabled, or services can be suspended if usage limits are reached.
- Free PostgreSQL expires after 30 days. It has no backups; after a further
  14-day grace period, Render deletes the database and its data.
- Free web services cannot send SMTP over ports 25, 465, or 587. Contact form
  submissions are still saved in PostgreSQL and can be reviewed in Django admin,
  but email notifications will fail. Use an HTTPS email API, an SMTP provider
  that supports a non-blocked port, or upgrade the web service before relying
  on notifications.
- To accommodate the free service's lack of shell and one-off jobs, the start
  command runs `migrate` before Gunicorn on every start. This is intended for
  this single-instance development setup, not as the production migration
  strategy.

Use a persistent paid database and an always-on paid web service before relying
on the site or its contact submissions. The production database setting
requires PostgreSQL and does not silently fall back to SQLite. Local
development continues to use SQLite unless `DATABASE_URL` is set. WhiteNoise
serves compressed static assets, and production security settings assume the
app is behind Render's HTTPS reverse proxy. HSTS subdomain coverage and browser
preloading remain disabled for Render's shared `onrender.com` domains; enable
them only after using a custom domain and confirming every subdomain is
HTTPS-only.
