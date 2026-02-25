import json
import threading
import time

from flask import Flask, Response, jsonify, render_template_string, request

app = Flask(__name__)

_lock = threading.Lock()
_latest = {
    "timestamp": None,
    "axes": {"left_x": 0.0, "left_y": 0.0, "right_x": 0.0, "right_y": 0.0},
    "buttons": [],
}
_config = {
    "deadzone": 0.08,
    "invert_y": True,
    "telemetry_hz": 30,
}

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Joystick Live View</title>
  <style>
    body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin: 2rem; }
    .card { border: 1px solid #bbb; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
    .row { margin: 0.4rem 0; }
    input[type="number"] { width: 6rem; }
  </style>
</head>
<body>
  <h1>Joystick Live View</h1>
  <div class="card">
    <div class="row"><strong>Status:</strong> <span id="status">waiting for telemetry...</span></div>
    <div class="row"><strong>Updated:</strong> <span id="updated">-</span></div>
    <pre id="axes">-</pre>
    <div class="row"><strong>Pressed Buttons:</strong> <span id="buttons">[]</span></div>
  </div>

  <div class="card">
    <h2>Config</h2>
    <form id="cfgForm">
      <div class="row">
        <label>Deadzone:
          <input id="deadzone" type="number" min="0" max="1" step="0.01" />
        </label>
      </div>
      <div class="row">
        <label>Telemetry Hz:
          <input id="telemetry_hz" type="number" min="1" max="120" step="1" />
        </label>
      </div>
      <div class="row">
        <label>Invert Y:
          <input id="invert_y" type="checkbox" />
        </label>
      </div>
      <button type="submit">Save Config</button>
      <span id="cfgResult"></span>
    </form>
  </div>

  <script>
    const statusEl = document.getElementById("status");
    const updatedEl = document.getElementById("updated");
    const axesEl = document.getElementById("axes");
    const buttonsEl = document.getElementById("buttons");

    const deadzoneEl = document.getElementById("deadzone");
    const telemetryHzEl = document.getElementById("telemetry_hz");
    const invertYEl = document.getElementById("invert_y");
    const cfgResultEl = document.getElementById("cfgResult");

    async function loadConfig() {
      const r = await fetch("/api/config");
      const cfg = await r.json();
      deadzoneEl.value = cfg.deadzone;
      telemetryHzEl.value = cfg.telemetry_hz;
      invertYEl.checked = cfg.invert_y;
    }

    const es = new EventSource("/stream");
    es.onmessage = (evt) => {
      const payload = JSON.parse(evt.data);
      const t = payload.timestamp;
      const axes = payload.axes || {};
      const buttons = payload.buttons || [];
      statusEl.textContent = t ? "live" : "waiting for telemetry...";
      updatedEl.textContent = t ? new Date(t * 1000).toLocaleTimeString() : "-";
      axesEl.textContent =
`Left  X: ${Number(axes.left_x || 0).toFixed(3)}
Left  Y: ${Number(axes.left_y || 0).toFixed(3)}
Right X: ${Number(axes.right_x || 0).toFixed(3)}
Right Y: ${Number(axes.right_y || 0).toFixed(3)}`;
      buttonsEl.textContent = JSON.stringify(buttons);
    };
    es.onerror = () => { statusEl.textContent = "stream disconnected"; };

    document.getElementById("cfgForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = {
        deadzone: Number(deadzoneEl.value),
        telemetry_hz: Number(telemetryHzEl.value),
        invert_y: invertYEl.checked
      };
      const r = await fetch("/api/config", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
      });
      cfgResultEl.textContent = r.ok ? " saved" : " failed";
      setTimeout(() => cfgResultEl.textContent = "", 1200);
    });

    loadConfig();
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/hi")
def hi():
    return "<p>hi there</p>"


@app.route("/api/telemetry", methods=["POST"])
def set_telemetry():
    payload = request.get_json(silent=True) or {}
    with _lock:
        _latest["timestamp"] = time.time()
        if "axes" in payload and isinstance(payload["axes"], dict):
            _latest["axes"] = payload["axes"]
        if "buttons" in payload and isinstance(payload["buttons"], list):
            _latest["buttons"] = payload["buttons"]
    return jsonify({"ok": True})


@app.route("/api/config", methods=["GET", "POST"])
def config_api():
    if request.method == "GET":
        with _lock:
            return jsonify(_config)

    payload = request.get_json(silent=True) or {}
    with _lock:
        if "deadzone" in payload:
            _config["deadzone"] = max(0.0, min(1.0, float(payload["deadzone"])))
        if "telemetry_hz" in payload:
            _config["telemetry_hz"] = max(1, min(120, int(payload["telemetry_hz"])))
        if "invert_y" in payload:
            _config["invert_y"] = bool(payload["invert_y"])
        return jsonify(_config)


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            with _lock:
                snapshot = dict(_latest)
                snapshot["axes"] = dict(_latest["axes"])
                snapshot["buttons"] = list(_latest["buttons"])
            yield f"data: {json.dumps(snapshot)}\n\n"
            time.sleep(0.1)

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
