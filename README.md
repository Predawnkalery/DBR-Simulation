# 🌟 Web-Based DBR & VCSEL Simulator

A full-stack physics simulation web application designed to calculate and visualise the optical reflectivity spectrum of Distributed Bragg Reflectors (DBRs) and Vertical-Cavity Surface-Emitting Lasers (VCSELs). 

This tool integrates directly with the public `refractiveindex.info` database to extract real-world optical constants ($n$, $k$) and utilises a custom Python-based Transfer Matrix Method (TMM) engine for precise optical modelling.


## ✨ Key Features

* **Live Database Integration:** dynamically fetches material properties from the `refractiveindex.info` catalog.
* **Dual Simulation Modes:**
  * **Single DBR Stack:** Simulates an alternating high/low index mirror on a substrate.
  * **Double DBR (VCSEL):** Simulates a full cavity sandwiched between top and bottom mirrors.
* **Transfer Matrix Method (TMM):** Robust Python/NumPy backend engine that calculates wavelength-dependent reflectivity.
* **Interactive Spectral Charting:** Visualizes the reflectivity spectrum using `Chart.js` with click-and-drag zoom functionality.
* **Dynamic Layer Visualisation:** Automatically generates a 2D scaled visual representation of the layer stack, mapping the refractive index ($n$) to colour gradients for intuitive analysis.
* **Workflow Optimisations:** Features a "Swap Material" toggle and a browser-cached "Pin to Top" favourites list for frequently used materials.

## 🛠️ Tech Stack
* **Backend:** Python, Flask, NumPy, Waitress
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Libraries/APIs:** `js-yaml` (parsing), `Chart.js` & `chartjs-plugin-zoom` (plotting), `refractiveindex` (database wrapper)

## 💻 Developer Guide

This section is for developers who want to clone, build, or modify the DBR Simulation Suite.

### 1. Set Up the Virtual Environment
It is highly recommended to use a virtual environment to isolate the project dependencies.

**For Mac/Linux:**
```bash 
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
````

**For Windows:**

Bash

```
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Fetch Offline Assets and Databases

This application is designed to be fully functional in air-gapped lab environments. Before running the server for the first time, you must download the required frontend JavaScript libraries and the master refractive index database catalog.

Run the offline setup script:

Bash

```
python make_offline.py
```

_Note: This script will automatically populate the `static/js/` and `static/data/` directories and download the `database_bundle.zip`._

### 3. Running the Application (Architecture Differences)

This project features two different entry points depending on your workflow:

**For Development & Debugging (`server.py`)**

When actively editing the codebase, run the raw Flask server. This bypasses the browser-automation wrapper, allowing you to see full Python tracebacks in the terminal and utilize standard web development tools.

Bash

```
python server.py
```

_Access via standard browser at: `http://127.0.0.1:5000`_

**For Production Testing (`desktop_app.py`)**

When testing the final user experience, use the desktop wrapper. This script spins up a robust `Waitress` production server on a background thread and automatically launches the user's default web browser. It is designed to keep the engine alive reliably during heavy matrix simulations without dropping the connection.

Bash

```
python desktop_app.py
```

_Automatically opens in default browser at: `http://127.0.0.1:8085`_

---

## 🎓 Team & Acknowledgements

This tool was developed as part of an academic research and design project.

- **Contributors:**
    
    - [Kriti Garg - IITD EE'26](https://github.com/Predawnkalery)
    - [Ishaan Lakhotiya - IITD EE'26]
        
- **Supervising Professor:** Prof. [Santanu Manna]
    
- **Institution:** [Department of Electrical Engineering, IIT Delhi]
    

_Special thanks to Mikhail Polyanskiy for maintaining the open-source [RefractiveIndex.INFO database](https://refractiveindex.info/)._

## 📄 License

**All Rights Reserved**

This software is currently proprietary and closed-source. It was developed for internal research and design purposes. Unauthorised copying, distribution, modification, or commercial use of this codebase is strictly prohibited without explicit written permission from the contributing authors and the supervising professor.

