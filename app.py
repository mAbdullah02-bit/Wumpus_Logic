"""
Flask API for Wumpus World Logic Agent
Serves the HTML page and provides JSON endpoints.
"""

from flask import Flask, jsonify, request, send_from_directory
import os, json
from wumpus_logic import run_episode, WumpusWorld, WumpusAgent

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def index():
    return send_from_directory("templates", "index.html")


@app.route("/api/run", methods=["POST"])
def api_run():
    data     = request.get_json(force=True)
    rows     = max(2, min(10, int(data.get("rows", 4))))
    cols     = max(2, min(10, int(data.get("cols", 4))))
    num_pits = data.get("num_pits", None)
    if num_pits is not None:
        num_pits = max(1, min(rows*cols-2, int(num_pits)))

    result = run_episode(rows, cols, num_pits)
    return jsonify(result)


@app.route("/api/step", methods=["POST"])
def api_step():
    """
    Stateless single-step: given current agent state + world state,
    compute next percepts + inferences.
    (Frontend manages the replay; this is used for live stepping.)
    """
    data = request.get_json(force=True)
    return jsonify({"status": "use /api/run for full episode"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
