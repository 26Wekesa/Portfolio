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

## Render static preview

The root [`render.yaml`](./render.yaml) defines a free Render Static Site.
`scripts/build_render_static_preview.py` copies the HTML pages and assets into
the publish directory and replaces the Django contact form with an email link.
This preview does not run Django, provide `/admin/`, store contact submissions,
or send form notifications.

After pushing changes to GitHub, open the `chris-tech-portfolio` Blueprint in
Render and choose **Manual sync**. This Blueprint uses the public repository
URL, so Render does not automatically deploy each push unless you connect your
GitHub account. The static site is globally served over HTTPS; Render's free
sites still count against workspace bandwidth and build usage limits.

For the full Django app, use a separate PostgreSQL database and a Render web
service. This workspace already has its single free PostgreSQL database in use
by another app, so the static preview avoids accessing or changing that data.
Local development continues to use SQLite unless `DATABASE_URL` is set.
