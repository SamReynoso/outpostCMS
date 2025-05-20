import time


def format_meta_diff(diff):
    print(diff)
    diff = diff.split("\n")
    html = "<dl>\n"
    start = False
    for line in diff:
        if line.find("}") != -1:
            start = False
            continue
        line = line.strip()
        if start:
            cols = [val.strip() for val in line.split('"')]
            if cols[0] == "":
                html += f"<dt>{cols[1]}</dt>\n"
                html += f"<dd>{cols[3]}</dd>\n"
            if cols[0] == "-":
                html += f"<dt class='delete'>{cols[1]}</dt>\n"
                html += f"<dd class='delete'> - {cols[3]}</dd>\n"
            if cols[0] == "+":
                html += f"<dt class='add'> {cols[1]}</dt>\n"
                html += f"<dd class='add'> + {cols[3]}</dd>\n"


        if line.startswith("@"):
            start = True

    html += "</dl>\n"
    return html


def format_index_diff(diff):
    html = '<article class="diff">\n'
        
    lines = diff.split("\n")
    start = False
    for line in lines:
        if line.startswith('@'):
            start = True
            continue
        if not start:
            continue
        if line.startswith('+'):
            cleaned = line[1:].strip()
            if cleaned.startswith("<"):
                start = cleaned.find(">")
                assert start != -1
                html += cleaned[:start] + ' class="add">' + cleaned[start + 1:]
            else:
                html += f'<span class="add">{cleaned}</span>\n'
            continue

        if line.startswith('-'):
            cleaned = line[1:].strip()
            if cleaned.startswith("<"):
                start = cleaned.find(">")
                assert start != -1, f"Start not found in {cleaned}"
                cleaned = cleaned[:start] + ' class="delete" ' + cleaned[start + 1:]
            else:
                html += f'<span class="delete">{cleaned}</span>\n'
            continue
        html += line + "\n"
        

    html += "</article>\n"
    return html
            


def new_site_map_entry(group: str, project_name: str, canonical: str):
    return {
        "group": group.strip(),
        "project_name": project_name.strip(),
        "canonical": canonical.strip(),
        "public": False,
    }


def new_metadata():
    date = time.strftime("%Y-%m-%d")
    return {
            "title": "Untitled",
            "description": "",
            "keywords": "",
            "author": "",
            "date": date,
            "last_updated": date,
            }
