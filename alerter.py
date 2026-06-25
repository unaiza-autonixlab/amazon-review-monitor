import smtplib
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_alerts(new_bad_reviews: list[dict], config: dict):
    if not new_bad_reviews:
        return

    if config.get("email", {}).get("enabled"):
        _send_email(new_bad_reviews, config["email"])

    if config.get("slack", {}).get("enabled"):
        _send_slack(new_bad_reviews, config["slack"]["webhook_url"])


def _send_email(reviews: list[dict], email_config: dict):
    subject = f"[Review Alert] {len(reviews)} new low-rated review(s) need attention"

    html_parts = []
    for r in reviews:
        stars = "⭐" * r["rating"]
        html_parts.append(f"""
        <div style="border-left:4px solid #e53e3e; padding:12px 16px; margin-bottom:20px; background:#fff5f5; border-radius:4px;">
            <p style="margin:0 0 4px 0; font-size:18px;">{stars} — <strong>{r['title']}</strong></p>
            <p style="margin:0 0 8px 0; color:#666; font-size:13px;">{r['author']} · {r['date']}</p>
            <p style="margin:0 0 10px 0; font-size:14px; color:#333;">{r['body'][:500]}{'...' if len(r['body']) > 500 else ''}</p>
            <p style="margin:0;"><strong>ASIN:</strong> {r['asin']} ·
            <a href="{r['url']}" style="color:#e53e3e;">View on Amazon →</a></p>
        </div>
        """)

    product_names = list({r.get("product_name", r["asin"]) for r in reviews})
    products_str = ", ".join(product_names)

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif; max-width:600px; margin:0 auto; padding:20px;">
        <h2 style="color:#e53e3e; margin-bottom:4px;">New low-rated reviews detected</h2>
        <p style="color:#666; margin-top:0;">Products: {products_str}</p>
        <hr style="border:none; border-top:1px solid #eee; margin:16px 0;">
        {''.join(html_parts)}
        <p style="color:#999; font-size:12px; margin-top:24px;">
            Sent by your Amazon Review Monitor. Respond within 24 hours to protect your seller rating.
        </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email_config["sender"]
    msg["To"] = ", ".join(email_config["recipients"])
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(email_config["smtp_host"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["sender"], email_config["password"])
            server.sendmail(
                email_config["sender"],
                email_config["recipients"],
                msg.as_string()
            )
        print(f"  [✓] Email sent to {email_config['recipients']}")
    except Exception as e:
        print(f"  [!] Email failed: {e}")


def _send_slack(reviews: list[dict], webhook_url: str):
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"🚨 {len(reviews)} new low-rated review(s)"}
        }
    ]

    for r in reviews:
        stars = "⭐" * r["rating"]
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{stars} {r['title']}*\n"
                    f"_{r['author']} · {r['date']}_\n"
                    f"{r['body'][:300]}{'...' if len(r['body']) > 300 else ''}\n"
                    f"ASIN: `{r['asin']}` · <{r['url']}|View on Amazon>"
                )
            }
        })
        blocks.append({"type": "divider"})

    payload = {"blocks": blocks}

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"  [✓] Slack alert sent")
    except Exception as e:
        print(f"  [!] Slack failed: {e}")
