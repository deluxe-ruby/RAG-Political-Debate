from flask import Flask, request, render_template, redirect, url_for, flash
import csv
import io

app = Flask(__name__)  # Initialize the Flask app
app.secret_key = "dev"  # You can change the secret key

@app.route('/configs/import', methods=['GET', 'POST'])
def import_configs():
    if request.method == 'POST':
        # Check if a file is part of the request
        file = request.files.get('file')
        if file:
            # Read the file content
            file_content = file.read().decode("utf-8")
            # Here, we'll try parsing the file as CSV for now
            try:
                reader = csv.DictReader(io.StringIO(file_content))
                new_configs = [] 
                for row in reader:
                    # Add the config to the list
                    new_configs.append({
                        'source_name': row.get('source_name'),
                        'url': row.get('url'),
                        'tags': row.get('tags'),
                        'source_type': row.get('source_type', 'Unknown')
                    })
                # Optionally, save to a file or database here
                source_configs.extend(new_configs)
                save_configs(source_configs)
                flash(f"Successfully imported {len(new_configs)} sources.")
                return redirect(url_for('list_configs'))
            except Exception as e:
                flash(f"Failed to parse the file: {str(e)}")
        else:
            flash("No file selected.")
    return render_template('configs/import.html')

# List all configs (used by View Sources buttons)
@app.route("/configs")
def list_configs():
    from flask import render_template
    import os
    import json

    config_dir = "configs"
    configs = []
    for filename in os.listdir(config_dir):
        if filename.endswith(".json"):
            with open(os.path.join(config_dir, filename)) as f:
                config = json.load(f)
                config['filename'] = filename
                configs.append(config)

    return render_template("configs/index.html", configs=configs)

# Redirect root URL to /configs
@app.route("/")
def index():
    from flask import redirect, url_for
    return redirect(url_for('list_configs'))
