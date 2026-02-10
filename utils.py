import re

def domain_from_url(url: str) -> str | None:
    if not isinstance(url, str) or not url.strip():
        return None
    u = url.strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = u.split("/")[0].split(":")[0]
    return u if "." in u else None

def domain_from_email(email: str) -> str | None:
    if not isinstance(email, str) or "@" not in email:
        return None
    return email.split("@", 1)[1].strip().lower()

def normalize_bool(x) -> bool:
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return bool(x)
    if isinstance(x, str):
        return x.strip().lower() in ("true", "yes", "1")
    return False

def detect_dns_host_from_spf(spf_record: str | None) -> str:
    if not spf_record:
        return "your DNS/email provider"
    s = spf_record.lower()
    if "spf.protection.outlook.com" in s or "mail.protection.outlook.com" in s:
        return "Microsoft 365"
    if "_spf.google.com" in s or "include:spf.google.com" in s:
        return "Google Workspace"
    if "amazonses" in s:
        return "Amazon SES"
    if "sendgrid.net" in s:
        return "SendGrid"
    if "mailgun.org" in s:
        return "Mailgun"
    return "your DNS/email provider"

def safe_company_from_domain(domain: str) -> str:
    base = (domain or "").split(".")[0]
    base = re.sub(r"[^a-zA-Z0-9]+", " ", base).strip()
    return base.title() if base else (domain or "")
