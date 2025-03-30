import json
import argparse
import os

CONFIG_FILE = "sources.json"

def load_sources():
    if not os.path.exists(CONFIG_FILE):
        return {"left_sources": {}, "right_sources": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_sources(sources):
    with open(CONFIG_FILE, "w") as f:
        json.dump(sources, f, indent=2)

def add_source(side, source_type, name, url):
    sources = load_sources()
    section = f"{side}_sources"
    if section not in sources:
        sources[section] = {}
    if source_type not in sources[section]:
        sources[section][source_type] = []
    sources[section][source_type].append({"name": name, "url": url})
    save_sources(sources)
    print(f"✅ Added source: {name} ({url}) to {side} → {source_type}")

def remove_source(url):
    sources = load_sources()
    for section in sources:
        for source_type in sources[section]:
            sources[section][source_type] = [
                s for s in sources[section][source_type] if s["url"] != url
            ]
    save_sources(sources)
    print(f"🗑️ Removed any sources matching: {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage scraping sources.")
    parser.add_argument("action", choices=["add", "remove"])
    parser.add_argument("--side", choices=["left", "right"], help="Left or right wing source")
    parser.add_argument("--type", help="substack, youtube, news, etc.")
    parser.add_argument("--name", help="Descriptive name of the source")
    parser.add_argument("--url", help="URL of the source")

    args = parser.parse_args()

    if args.action == "add":
        if not all([args.side, args.type, args.name, args.url]):
            print("❌ For 'add', you must provide --side, --type, --name, and --url.")
        else:
            add_source(args.side, args.type, args.name, args.url)
    elif args.action == "remove":
        if not args.url:
            print("❌ For 'remove', you must provide --url.")
        else:
            remove_source(args.url)
