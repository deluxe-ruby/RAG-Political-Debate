@app.route('/configs')
def list_configs():
    filter_tag = request.args.get("tag")
    filter_type = request.args.get("type")
    query = request.args.get("q", "").lower()
    sort = request.args.get("sort", "")

    filtered_configs = []
    for config in source_configs:
        tags = config.get("tags", "")
        combined = f"{config['source_name']} {config['url']} {tags}".lower()
        if query and query not in combined:
            continue

        actual_type = config.get("source_type") or "Unknown"
        if filter_type and actual_type != filter_type:
            continue

        filtered_configs.append(config)

    if sort == "name_asc":
        filtered_configs.sort(key=lambda c: c["source_name"].lower())
    elif sort == "name_desc":
        filtered_configs.sort(key=lambda c: c["source_name"].lower(), reverse=True)
    elif sort == "type":
        filtered_configs.sort(key=lambda c: (c.get("source_type") or "Unknown").lower())

    return render_template('configs/index.html',
        configs=filtered_configs,
        filter_tag=filter_tag,
        filter_type=filter_type,
        query=query,
        sort=sort
    )
@app.route('/configs')
def list_configs():
    filter_tag = request.args.get("tag")
    filter_type = request.args.get("type")
    query = request.args.get("q", "").lower()
    sort = request.args.get("sort", "")

    filtered_configs = []
    for config in source_configs:
        tags = config.get("tags", "")
        combined = f"{config['source_name']} {config['url']} {tags}".lower()
        if query and query not in combined:
            continue

        actual_type = config.get("source_type") or "Unknown"
        if filter_type and actual_type != filter_type:
            continue

        config['source_type'] = actual_type  # 🟡 Patch missing ones for display
        filtered_configs.append(config)

    if sort == "name_asc":
        filtered_configs.sort(key=lambda c: c["source_name"].lower())
    elif sort == "name_desc":
        filtered_configs.sort(key=lambda c: c["source_name"].lower(), reverse=True)
    elif sort == "type":
        filtered_configs.sort(key=lambda c: c.get("source_type", "Unknown").lower())

    return render_template('configs/index.html',
        configs=filtered_configs,
        filter_tag=filter_tag,
        filter_type=filter_type,
        query=query,
        sort=sort
    )
