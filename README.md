# gaze_audio_project
A software-based gaze detection system that automatically switches audio output to the screen you’re looking at — no extra hardware.

Infostrom — Gaze-Driven Selective Audio Project (IBM LinuxOne)
Overview

Infostrom is an interactive Jupyter notebook demo that simulates gaze-driven audio focus using simple face-position logic.
This version is specifically designed for online Jupyter environments where direct webcam access may be limited or unavailable.

The demo illustrates how gaze estimation can be used to selectively activate or focus audio streams, mimicking how a system might dynamically adjust audio based on where a user is looking.

🎯 Purpose

To provide an interactive simulation of a gaze-controlled audio environment, demonstrating:

Face-position–based "gaze" detection.

Zone-based focus logic across multiple monitors.

Real-time visual feedback of active focus and audio simulation.

🧩 Features

✅ Inline frame display — Runs entirely inside a Jupyter Notebook (no external GUI windows required).

🖥️ 8 virtual monitors — The display is divided into eight logical zones, representing different screens or audio sources.

👁️ Simple face-position gaze estimation — The position of a detected face determines which monitor zone is currently “looked at.”

🔊 Visual and simulated audio feedback — The active monitor is highlighted, and its simulated audio status (on/off) is displayed.

⚙️ Requirements

Python 3.x

Jupyter Notebook or JupyterLab

OpenCV

NumPy

(Optional) Audio simulation or placeholder logic

🚀 Usage

Open the notebook in Jupyter.

Run all cells to initialize the environment.

If webcam access is restricted, use simulated face positions or static image input.

Observe the visual indicators showing which “monitor” is currently active and the corresponding simulated audio focus.

🧠 Conceptual Flow

Face Detection → Detect or simulate face coordinates.

Zone Mapping → Determine which of the 8 virtual monitors the face is pointing toward.

Focus Simulation → Visually and logically activate the corresponding audio source.

📦 Notes

This version avoids the use of external windows or GUI dependencies to ensure compatibility with cloud-based and sandboxed environments (e.g., IBM LinuxOne, JupyterHub, or Google Colab).

Future versions may integrate with real gaze-tracking APIs and spatial audio systems.

🧑‍💻 Authors & Acknowledgements

Developed as part of the IBM Z Datathon.
Inspired by gaze-driven interfaces and selective attention models in human-computer interaction.
