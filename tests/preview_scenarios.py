"""Local synthetic UI checks without replacing the checked-in demonstration.

Run: PYTHONPATH=src python3.11 tests/preview_scenarios.py --port 8772
Visit /, /empty/, /negative/, /small/, or /missing-condition/.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from copy import deepcopy
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from liveforever_lab.analysis import analyze_dataset
from liveforever_lab.care_brief import build_care_brief, export_care_brief
from liveforever_lab.planner import build_plan
from liveforever_lab.synthetic import DEMO_PROVENANCE, generate_records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8772)
    args = parser.parse_args()
    demo = Path(__file__).resolve().parents[1] / "demo"
    scenarios = {}
    for name in ("empty", "negative", "small", "missing-condition"):
        records = [] if name == "empty" else generate_records(days=6 if name == "small" else 84)
        for row in records:
            if name == "negative" and row["hrv_ms"] is not None:
                row["hrv_ms"] = 100 - row["hrv_ms"]
            if name == "missing-condition":
                row["caffeine_cutoff_2pm"] = 1
        provenance = deepcopy(DEMO_PROVENANCE)
        for source in provenance["sources"].values():
            source.update(url=f"http://127.0.0.1:{args.port}/{name}/records.csv", provenance=f"Synthetic {name} regression scenario generated in memory by tests/preview_scenarios.py.")
        analysis = analyze_dataset(records, provenance=provenance)
        plan = build_plan(analysis)
        brief = build_care_brief(analysis, plan)
        payload = {"analysis": analysis, "plan": plan, "care_brief": brief, "exports": {"care_brief_markdown": export_care_brief(brief, "markdown")}}
        stream = io.StringIO()
        if records:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
        scenarios[name] = {"analysis.json": json.dumps(payload).encode(), "records.csv": stream.getvalue().encode()}

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *positional, **kwargs):
            super().__init__(*positional, directory=str(demo), **kwargs)

        def do_GET(self):
            pieces = self.path.split("?", 1)[0].strip("/").split("/", 1)
            if pieces[0] in scenarios:
                name, asset = pieces[0], pieces[1] if len(pieces) > 1 else ""
                if asset in scenarios[name]:
                    content = scenarios[name][asset]
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json" if asset.endswith("json") else "text/csv")
                    self.send_header("Content-Length", str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)
                    return
                self.path = "/" + asset
            super().do_GET()

    print(f"Synthetic UI checks: http://127.0.0.1:{args.port}/ (empty, negative, small, missing-condition paths)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
