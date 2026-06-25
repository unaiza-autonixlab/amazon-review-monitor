#!/usr/bin/env python3
"""
Amazon Review Monitor
Checks for new reviews below your rating threshold and alerts you immediately.
Run this on a schedule (every 2-4 hours) to catch bad reviews before your client does.
"""

import json
import os
import sys
from datetime import datetime
from scraper import fetch_recent_reviews
from alerter import send_alerts

CONFIG_FILE = "config.json"
SEEN_FILE = "seen_reviews.json"


def load_json(path: str, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default


def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    config = load_json(CONFIG_FILE, {})
    if not config:
        print("[!] No config found. Copy config.example.json to config.json and fill it in.")
        sys.exit(1)

    api_token = config.get("apify_token", "")
    if not api_token or api_token.startswith("apify_api_XXX"):
        print("[!] Add your Apify API token to config.json.")
        print("    Get one free at: https://apify.com (no credit card required)")
        sys.exit(1)

    threshold = config.get("alert_threshold", 3)
    seen_ids: set = set(load_json(SEEN_FILE, []))
    products = config.get("products", [])

    if not products:
        print("[!] No products listed in config.json")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"Amazon Review Monitor | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Monitoring {len(products)} product(s) | Alert threshold: {threshold} stars or below")
    print(f"{'='*50}\n")

    new_bad_reviews = []

    for product in products:
        asin = product["asin"]
        name = product.get("name", asin)
        print(f"Checking: {name} ({asin})")

        reviews = fetch_recent_reviews(asin, api_token)
        print(f"  Found {len(reviews)} recent review(s)")

        for review in reviews:
            if review["id"] in seen_ids:
                continue

            seen_ids.add(review["id"])

            if review["rating"] <= threshold:
                review["product_name"] = name
                new_bad_reviews.append(review)
                print(f"  [!] NEW {review['rating']}star review: {review['title'][:60]}")

    if new_bad_reviews:
        print(f"\nSending alerts for {len(new_bad_reviews)} new low-rated review(s)...")
        send_alerts(new_bad_reviews, config)
    else:
        print("\nAll clear. No new low-rated reviews.")

    save_json(SEEN_FILE, list(seen_ids))
    print(f"\nDone. {len(seen_ids)} total reviews tracked.\n")


if __name__ == "__main__":
    main()
