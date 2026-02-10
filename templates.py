"""
Scenario templates based on your LLM Script scenarios (1–5),
with the Dark Web sections removed (no usernames/passwords/dates).

Scenarios:
1) DMARC flawed (p=none/weak), SPF & DKIM correct
2) SPF missing
3) SPF missing + DMARC missing
4) DKIM missing
5) SPF, DKIM, DMARC all missing
"""

def render_template(scenario: int, name: str, domain: str, dns_host: str, phone: str, company: str | None = None):
    name = name.strip() if name else "there"
    company = (company or domain).strip()

    if scenario == 1:
        subject = f"Security gap detected for {domain} (DMARC not enforced)"
        plain = f"""Hi {name},

We’re a cybersecurity firm and need to make you aware of an email authentication gap for {domain}.
This may be a result of your DNS security settings at {dns_host} not being properly configured.

Here’s what we found regarding your email authentication:
• SPF (Authorized Mail Sender): Configured correctly
• DKIM (Ensures Mail Encryption): Configured correctly
• DMARC (Handling Malicious Mail): Implemented but not enforced (p=none / weak)

A DMARC policy set to “none” means failed emails aren’t blocked — they’re just monitored.
When DMARC isn’t enforced, it becomes much easier for attackers to impersonate your domain and trick users.

If you want to learn more, or have this fixed, either reply to this email or call us at {phone}.
"""
    elif scenario == 2:
        subject = f"High-risk email issue for {domain}: SPF missing"
        plain = f"""Hi {name},

We’re a cybersecurity firm and need to make you aware of an email authentication gap for {domain}.
This may be a result of your DNS security settings at {dns_host} not being properly configured.

Here’s what our scan found:
• SPF (Authorized Mail Sender): Missing
• DKIM (Ensures Mail Encryption): Configured correctly
• DMARC (Handling Malicious Mail): Configured correctly

SPF tells email providers which servers are allowed to send mail for your domain.
Without it, attackers can impersonate your staff or your brand.

If you want to learn more, or have this fixed, either reply to this email or call us at {phone}.
"""
    elif scenario == 3:
        subject = f"Critical email security gaps for {domain}: SPF + DMARC missing"
        plain = f"""Hi {name},

We’re a cybersecurity firm and need to make you aware of critical email authentication gaps for {domain}.
This may be a result of your DNS security settings at {dns_host} not being properly configured.

Here’s what we found:
• SPF (Authorized Mail Sender): Missing
• DMARC (Handling Malicious Mail): Missing
• DKIM (Ensures Mail Encryption): Configured correctly

Without SPF and DMARC, attackers can impersonate any employee and mail providers will treat those fraudulent messages as legitimate.

If you want to learn more, or have this fixed, either reply to this email or call us at {phone}.
"""
    elif scenario == 4:
        subject = f"Your domain {domain} is missing DKIM"
        plain = f"""Hi {name},

We’re a cybersecurity firm and need to make you aware of an email authentication gap for {domain}.
This may be a result of your DNS security settings at {dns_host} not being properly configured.

Here’s what we discovered:
• SPF (Authorized Mail Sender): Configured correctly
• DKIM (Ensures Mail Encryption): Missing
• DMARC (Handling Malicious Mail): Configured correctly

Without DKIM, receiving mail systems cannot verify that messages weren’t forged or altered.

If you want to learn more, or have this fixed, either reply to this email or call us at {phone}.
"""
    elif scenario == 5:
        subject = f"Critical security failures for {domain}: SPF, DKIM, DMARC missing"
        plain = f"""Hi {name},

We’re a cybersecurity firm and need to make you aware of critical email authentication failures for {domain}.
This may be a result of your DNS security settings at {dns_host} not being properly configured.

Here’s what our scan found:
• SPF (Authorized Mail Sender): Missing
• DKIM (Ensures Mail Encryption): Missing
• DMARC (Handling Malicious Mail): Missing

With all three protections missing, attackers can impersonate any employee and deliver emails that appear entirely legitimate.

If you want to learn more, or have this fixed, either reply to this email or call us at {phone}.
"""
    else:
        subject = f"Email authentication check for {domain}"
        plain = f"""Hi {name},

We ran an email-authentication scan for {domain}. If you'd like a brief summary and recommendations, reply to this email.

If you want to learn more, either reply to this email or call us at {phone}.
"""

    html = "<html><body>" + "<br>".join(plain.splitlines()) + "</body></html>"
    return subject, plain, html
