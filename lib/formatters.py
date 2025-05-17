
def format_branch(**entry):
    return entry['group'] + '/' + entry['project_name'] 


def format_meta_diff(diff):
    diff = diff.split("\n")
    html = "<dl>\n"
    start = False
    for i, line in enumerate(diff):
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
                html += f"<dt class='deleted'> - {cols[1]}</dt>\n"
                html += f"<dd class='deleted'> - {cols[3]}</dd>\n"
            if cols[0] == "+":
                html += f"<dt class='added'>+ {cols[1]}</dt>\n"
                html += f"<dd class='added'>+ {cols[3]}</dd>\n"


        if line.startswith("{"):
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
                cleaned = cleaned[:start] + ' class="add">' + cleaned[start + 1:]
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
            
