# Amazon Review Monitor

Get alerted the moment a client's product gets a bad review. Before they do.

Checks Amazon every few hours. Sends you an email or Slack message for any new review at or below your rating threshold (default: 3 stars).

Free to use. Requires a free Apify account (no credit card needed) to pull Amazon review data reliably.

---

## What you get

- Email alert with the full review text, star rating, reviewer name, and a direct link
- Slack alert if you prefer
- Tracks which reviews you have already seen so you never get duplicate alerts
- Covers as many ASINs as you want across any number of clients

---

## Setup (5 minutes)

**Step 1: Get a free Apify account**
Sign up at apify.com. No credit card required. Free tier gives you $5/month in credits, which is enough to monitor 20-30 ASINs checked every few hours.

Once signed in, go to Settings → Integrations → copy your API token.

**Step 2: Install Python**
Download from python.org if you don't have it. Any version 3.10 or higher works.

**Step 3: Install dependencies**
```
pip install -r requirements.txt
```

**Step 4: Create your config file**
Copy `config.example.json` to `config.json` and fill in:
- Your Apify API token
- Your client ASINs (find these in the Amazon product page URL)
- Your email or Slack settings for alerts

**Step 5: Run it once to test**
```
python monitor.py
```

You should see it check each ASIN and print what it found.

**Step 6: Schedule it**
Run this every 2-4 hours so you catch reviews fast.

On Windows (Task Scheduler):
- Open Task Scheduler, click Create Basic Task
- Trigger: Daily, repeat every 2 hours
- Action: Start a program, set program to `python`
- Arguments: `C:\path\to\review-alert\monitor.py`
- Start in: `C:\path\to\review-alert\`

On Mac/Linux (cron):
```
0 */2 * * * cd /path/to/review-alert && python monitor.py
```

---

## Free tier limits

On a free Apify account, each run returns up to 10 recent reviews per ASIN. This is enough to catch new bad reviews as they come in. If you need deeper history or higher volume, upgrading to a paid Apify plan removes the limit.

---

## Gmail setup

Gmail requires an App Password (not your regular password).

1. Go to myaccount.google.com, then Security, then 2-Step Verification (enable it)
2. Go back to Security, then App Passwords
3. Create one for Mail
4. Use that 16-character password in config.json

---

## Adding more clients

Add more ASINs to the `products` array in config.json:

```json
{
  "asin": "B0XXXXXXXXX",
  "name": "Brand Name, Product Name"
}
```

Each ASIN is checked in a separate Apify run.

---

## Alert threshold

Default is 3 stars (alerts on 1, 2, and 3 star reviews).

Change `alert_threshold` in config.json to 4 if you want to catch anything below 4 stars.

---

Built by Autonix Lab · autonixlab.com
