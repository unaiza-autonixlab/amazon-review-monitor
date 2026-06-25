# Amazon Review Monitor

Get alerted the moment a client's product gets a bad review. Before they do.

Checks Amazon every few hours. Sends you an email or Slack message for any new review at or below your rating threshold (default: 3 stars).

No paid tools. No API keys. Just Python.

---

## What you get

- Email alert with the full review text, star rating, reviewer name, and a direct link
- Slack alert if you prefer
- Tracks which reviews you've already seen so you never get duplicate alerts
- Covers as many ASINs as you want across any number of clients

---

## Setup (5 minutes)

**Step 1 — Install Python**
Download from python.org if you don't have it. Any version 3.10+ works.

**Step 2 — Install dependencies**
```
pip install -r requirements.txt
```

**Step 3 — Create your config file**
Copy `config.example.json` to `config.json` and fill in:
- Your client's ASINs (find these on the Amazon product page URL)
- Your email settings (Gmail works best — see note below)
- Or your Slack webhook URL if you prefer Slack

**Step 4 — Run it once to test**
```
python monitor.py
```

You should see it check each ASIN and print what it found.

**Step 5 — Schedule it**
Run this every 2-4 hours so you catch reviews fast.

*On Windows (Task Scheduler):*
- Open Task Scheduler → Create Basic Task
- Trigger: Daily, repeat every 2 hours
- Action: Start a program → `python`
- Arguments: `C:\path\to\review-alert\monitor.py`
- Start in: `C:\path\to\review-alert\`

*On Mac/Linux (cron):*
```
0 */2 * * * cd /path/to/review-alert && python monitor.py
```

---

## Gmail setup

Gmail requires an App Password (not your regular password).

1. Go to myaccount.google.com → Security → 2-Step Verification (enable it)
2. Then go to Security → App Passwords
3. Create one for "Mail"
4. Use that 16-character password in config.json

---

## Adding more clients

Just add more ASINs to the `products` array in config.json:

```json
{
  "asin": "B0XXXXXXXXX",
  "name": "Brand Name — Product Name"
}
```

No limit on how many you add.

---

## Alert threshold

Default is 3 stars (alerts on 1, 2, and 3 star reviews).

Change `alert_threshold` in config.json to 4 if you want to catch anything below 4 stars.

---

Built by Autonix Lab — autonixlab.com
