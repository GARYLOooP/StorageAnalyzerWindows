"""Inject an analysis JSON into the HTML template -> a standalone report.

Usage:
    build_report.py <analysis.json> [output.html]

The analysis JSON is produced by the AI agent. Schema is documented in
SKILL.md Appendix B (inline template with concrete examples).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "report_template.html")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser(
        os.path.join(os.environ.get("USERPROFILE", "~"), "Desktop",
                     "storage-report.html"))

    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        tpl = f.read()

    blob = json.dumps(data, ensure_ascii=False)
    # Static report has no delete capability (DELETE=null).
    # Delete buttons only appear when served via server.py.
    html = tpl.replace("__REPORT_DATA__", blob)\
              .replace("__DELETE_CONFIG__", "null")

    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report generated: {out}")


if __name__ == "__main__":
    main()
