import argparse
import json
import os

CONFIG_FILE = "sources.json"

def load_sources():
    if not os.path.exists(CONFIG_FILE):
        return {"left_sources": {}, "right_sources": {}}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_sources(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_source(side, source_type, name, url, tags=None, category=None):
    data = load_sources()
    side_key = f"{side}_sources"
    if side_key not in data:
        data[side_key] = {}
    if source_type not in data[side_key]:
        data[side_key][source_type] = []

    new_entry = {
        "name": name,
        "url": url
    }

    if tags:
        new_entry["tags"] = [tag.strip() for tag in tags.split(",")]
    if category:
        new_entry["category"] = category

    data[side_key][source_type].append(new_entry)
    save_sources(data)
    print(f"✅ Added {name} to {side_key}/{source_type}")

def remove_source(name):
    data = load_sources()
    removed = False
    for side in ["left_sources", "right_sources"]:
        for source_type in data.get(side, {}):
            original_len = len(data[side][source_type])
            data[side][source_type] = [s for s in data[side][source_type] if s["name"] != name]
            if len(data[side][source_type]) != original_len:
                removed = True
                print(f"🗑️ Removed {name} from {side}/{source_type}")
    if removed:
        save_sources(data)
    else:
        print(f"⚠️ Source '{name}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage scraping sources.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--side", required=True, choices=["left", "right"])
    add_parser.add_argument("--type", required=True, choices=["youtube", "website", "podcast"])
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--url", required=True)
    add_parser.add_argument("--tags", required=False)
    add_parser.add_argument("--category", required=False)

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("--name", required=True)

    args = parser.parse_args()

    if args.command == "add":
        add_source(args.side, args.type, args.name, args.url, args.tags, args.category)
    elif args.command == "remove":
        remove_source(args.name)
    else:
        parser.print_help()
