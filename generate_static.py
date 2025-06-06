from news_dashboard import index
import os

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

html_content = index()
with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Static HTML generated in /output/index.html")
