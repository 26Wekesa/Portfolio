import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PUBLISH_DIR = ROOT / "render-static"
CONTACT_FORM = re.compile(
    r"""(?P<indent>^[ \t]*)<form action="\{% url 'contact_submit' %\}" """
    r"""method="post" class="php-email-form".*?</form><!-- End Contact Form -->""",
    re.MULTILINE | re.DOTALL,
)


def main():
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        raise RuntimeError("No HTML pages found to publish.")

    if PUBLISH_DIR.exists():
        if not PUBLISH_DIR.is_dir():
            raise RuntimeError(f"Static output path is not a directory: {PUBLISH_DIR}")
        shutil.rmtree(PUBLISH_DIR)
    PUBLISH_DIR.mkdir()

    for page in pages:
        content = page.read_text(encoding="utf-8")
        if page.name == "contact.html":
            content, replacements = CONTACT_FORM.subn(
                lambda match: (
                    f'{match.group("indent")}<div class="text-center">'
                    '<p class="alert alert-info">The contact form is disabled in this '
                    'preview. Email <a href="mailto:wekesachristopher@gmail.com">'
                    "wekesachristopher@gmail.com</a> to get in touch.</p></div>"
                    "<!-- End Contact Form -->"
                ),
                content,
                count=1,
            )
            if replacements != 1:
                raise RuntimeError("Could not safely disable the contact form.")
            content = content.replace(
                '  <script defer src="assets/vendor/php-email-form/validate.js"></script>\n',
                "",
            )

        if "{%" in content or "{{" in content:
            raise RuntimeError(f"Unrendered Django template syntax in {page.name}.")
        (PUBLISH_DIR / page.name).write_text(content, encoding="utf-8")

    assets = ROOT / "assets"
    if not assets.is_dir():
        raise FileNotFoundError(f"Static assets directory not found: {assets}")
    shutil.copytree(assets, PUBLISH_DIR / "assets")
    print(f"Prepared {len(pages)} static pages and assets in {PUBLISH_DIR}.")


if __name__ == "__main__":
    main()
