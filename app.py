import streamlit as st
import numpy as np
import cv2
import time
from math import sin

# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="AI Gaze Visualization Dashboard",
    layout="wide"
)

# ============================================================
# Session State
# ============================================================
if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.speed = 50
    st.session_state.num_monitors = 8
    st.session_state.gaze_pattern = "mouse"
    st.session_state.frame = np.zeros((400, 640, 3), np.uint8)
    st.session_state.monitor_idx = None
    st.session_state.trail = []
    st.session_state.mouse_x = 0.5
    st.session_state.mouse_y = 0.5
    st.session_state.target_x = 0.5
    st.session_state.keyboard_x = 0.5
    st.session_state.fps = 0
    st.session_state.logs = []
    st.session_state.last_time = time.time()

# ============================================================
# Logging
# ============================================================
def log(msg):
    st.session_state.logs.append(msg)
    if len(st.session_state.logs) > 50:
        st.session_state.logs.pop(0)

# ============================================================
# Sidebar Controls
# ============================================================
st.sidebar.title("🎛 Controls")

st.sidebar.button("▶ Start", on_click=lambda: log("🟢 Simulation started.") or setattr(st.session_state, "running", True))
st.sidebar.button("⏸ Pause", on_click=lambda: setattr(st.session_state, "running", False))
st.sidebar.button("⏹ Stop", on_click=lambda: (
    setattr(st.session_state, "running", False),
    setattr(st.session_state, "monitor_idx", None)
))
st.sidebar.button("🔁 Reset", on_click=lambda: (
    setattr(st.session_state, "running", False),
    st.session_state.trail.clear(),
    setattr(st.session_state, "mouse_x", 0.5),
    setattr(st.session_state, "mouse_y", 0.5),
    setattr(st.session_state, "target_x", 0.5),
    setattr(st.session_state, "keyboard_x", 0.5),
    log("🔁 Reset complete.")
))

st.sidebar.slider(
    "Speed (ms)",
    10, 200,
    st.session_state.speed,
    step=5,
    key="speed"
)

st.sidebar.slider(
    "Monitors",
    2, 8,
    st.session_state.num_monitors,
    step=1,
    key="num_monitors"
)

st.sidebar.selectbox(
    "Mode",
    ["mouse", "keyboard", "sine", "linear", "zigzag"],
    key="gaze_pattern"
)

# Mouse approximation
if st.session_state.gaze_pattern == "mouse":
    st.sidebar.slider(
        "Mouse X",
        0.0, 1.0,
        st.session_state.target_x,
        key="target_x"
    )
    st.sidebar.slider(
        "Mouse Y",
        0.0, 1.0,
        st.session_state.mouse_y,
        key="mouse_y"
    )

# Keyboard mode buttons
if st.session_state.gaze_pattern == "keyboard":
    col1, col2 = st.sidebar.columns(2)
    if col1.button("⬅ Left"):
        st.session_state.keyboard_x = max(0.0, st.session_state.keyboard_x - 0.05)
    if col2.button("➡ Right"):
        st.session_state.keyboard_x = min(1.0, st.session_state.keyboard_x + 0.05)

# ============================================================
# Simulation Step
# ============================================================
def simulate_step():
    s = st.session_state

    # Gaze modes
    if s.gaze_pattern == "mouse":
        gx = s.target_x
    elif s.gaze_pattern == "keyboard":
        gx = s.keyboard_x
    elif s.gaze_pattern == "sine":
        gx = (sin(time.time() * 0.7) + 1) / 2
    elif s.gaze_pattern == "linear":
        gx = (time.time() * 0.25) % 1.0
    elif s.gaze_pattern == "zigzag":
        t = (time.time() * 0.5) % 2
        gx = t if t <= 1 else 2 - t
    else:
        gx = 0.5

    # Smooth motion
    s.mouse_x += (gx - s.mouse_x) * 0.25

    # Monitor grid
    cols = 4
    rows = int(np.ceil(s.num_monitors / cols))
    mw = 640 // cols
    mh = 400 // rows

    idx = min(int(s.mouse_x * s.num_monitors), s.num_monitors - 1)
    s.monitor_idx = idx

    f = np.zeros((400, 640, 3), np.uint8)
    pulse = (sin(time.time() * 4) + 1) / 2

    for i in range(s.num_monitors):
        r, c = divmod(i, cols)
        x1, y1 = c * mw, r * mh
        x2, y2 = x1 + mw, y1 + mh
        color = (int(80 + 150 * pulse), int(255 * pulse), 0) if i == idx else (70, 70, 70)
        cv2.rectangle(f, (x1, y1), (x2, y2), color, 2)
        cv2.putText(f, str(i + 1), (x1 + 8, y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

    cx = int(s.mouse_x * 640)
    cy = int(s.mouse_y * 400) if s.gaze_pattern == "mouse" else 200 + int(sin(time.time() * 3) * 60)

    s.trail.append((cx, cy))
    if len(s.trail) > 12:
        s.trail.pop(0)

    for i, (tx, ty) in enumerate(s.trail):
        a = i / len(s.trail)
        cv2.circle(f, (tx, ty), 5, (0, int(255 * a), int(255 * (1 - a))), -1)

    cv2.circle(f, (cx, cy), 10, (0, 255, 255), -1)

    now = time.time()
    s.fps = 1 / (now - s.last_time) if now > s.last_time else 0
    s.last_time = now

    s.frame = f

# ============================================================
# Main Layout
# ============================================================
st.markdown("## 👁️ AI Gaze Visualization Dashboard")

status = "🟢 Running" if st.session_state.running else "🔴 Stopped"
st.markdown(
    f"**Status:** {status} | "
    f"**Monitor:** {st.session_state.monitor_idx} | "
    f"**Mode:** {st.session_state.gaze_pattern} | "
    f"**FPS:** {int(st.session_state.fps)}"
)

# Run simulation
if st.session_state.running:
    simulate_step()
    time.sleep(st.session_state.speed / 1000)
    st.experimental_rerun()

# Display frame
st.image(
    cv2.cvtColor(st.session_state.frame, cv2.COLOR_BGR2RGB),
    width=640
)

# Logs
st.markdown("### 📋 Event Log")
st.code("\n".join(st.session_state.logs), language="text")
