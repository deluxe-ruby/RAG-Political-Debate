
@app.route('/configs/confirm_import', methods=['POST'])
def confirm_import():
    import_data = request.form.get("import_data")
    if not import_data:
        flash("No import data received.")
        return redirect(url_for('list_configs'))

    try:
        new_configs = json.loads(import_data)
        for item in new_configs:
            item['source_type'] = item.get('source_type') or detect_source_type(item.get('url', ''))
            source_configs.append(item)
        save_configs(source_configs)
        flash(f"Successfully imported {len(new_configs)} sources.")
    except Exception as e:
        flash("Import failed.")
        print("Import error:", e)

    return redirect(url_for('list_configs'))
