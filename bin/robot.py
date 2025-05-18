import json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

PARENT_DIR = Path(__file__).parent.parent
print( f"Parent directory: {PARENT_DIR}")

CANON_DIR = PARENT_DIR.joinpath("canonical")

BASE_URL = "https://ozprealpha.com"
ROUTE_PREFIX = "/archive/" 
INPUT_JSON = Path(CANON_DIR) / "articles.json"
OUTPUT_XML = Path(CANON_DIR) / "sitemap.xml"
OUTPUT_ROBOT= Path(CANON_DIR) / "robots.txt"

try:
    with INPUT_JSON.open() as f:
        articles = json.load(f)
except FileNotFoundError:
    print(f"Error: {INPUT_JSON} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: {INPUT_JSON} is not a valid JSON file.")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

robot_lines = [
    "User-agent: *",
    "Disallow:",
    "",
    f"Sitemap: {BASE_URL}/sitemap.xml",
    "",
]

urlset = Element("urlset")
urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

for article in articles:
    slug = article["canonical"]
    robot_lines.append(f"Allow: {ROUTE_PREFIX}{slug}")
    url = SubElement(urlset, "url")
    loc = SubElement(url, "loc")
    loc.text = f"{BASE_URL}{ROUTE_PREFIX}{article['slug']}"
    lastmod = SubElement(url, "lastmod")
    lastmod.text = article["date"]

raw_xml = tostring(urlset, "utf-8")
pretty_xml = xml.dom.minidom.parseString(raw_xml).toprettyxml(indent="  ")

try:
    OUTPUT_ROBOT.write_text("\n".join(robot_lines) + "\n")
    OUTPUT_XML.write_text(pretty_xml)
except Exception as e:
    print(f"Error writing to output files: {e}")
    exit(1)

print(f'''
Sitemap and robots.txt generated successfully!
    Articles found: {len(articles)}

    Writing files:
        robots.txt
        sitemap.xml 
      ''')
