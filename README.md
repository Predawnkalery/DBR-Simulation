# 🌟 Web-Based DBR & VCSEL Simulator

A full-stack physics simulation web application designed to calculate and visualise the optical reflectivity spectrum of Distributed Bragg Reflectors (DBRs) and Vertical-Cavity Surface-Emitting Lasers (VCSELs). 

This tool integrates directly with the public `refractiveindex.info` database to extract real-world optical constants ($n$, $k$) and utilises a custom Python-based Transfer Matrix Method (TMM) engine for precise optical modelling.

Direct web access available at our primary URL https://dbr-simulation-suite.onrender.com

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
* **Backend:** Python, Flask, NumPy
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Libraries/APIs:** `js-yaml` (parsing), `Chart.js` & `chartjs-plugin-zoom` (plotting), `refractiveindex` (database wrapper)


## 🚀 Installation & Local Setup 
### Using local Package 

The standard workflow for a researcher receiving your ZIP file would look like this:

1. Unzip the folder.
2. Open terminal and run: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install libraries: `pip install -r requirements.txt`
5. Run the app: `python server.py` (This is the step where your new script silently unpacks the database bundle).

### Using github repo

**1. Clone the repository:**
```bash
git clone https://github.com/Predawnkalery/DBR-Simulation-Suite.git
cd DBR-Simulation-Suite
```

**2. Set up a virtual environment (Recommended):**
* Mac/Linux: `python3 -m venv venv && source venv/bin/activate`
* Windows: `python -m venv venv && venv\Scripts\activate`

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the development server:**
Before running the dev server, ensure uncommenting the last line of code in server.py
```bash
python server.py
```
*Navigate to `http://127.0.0.1:5000` in your web browser.*

## 📂 Project Structure
```text
/
├── server.py              # Main Flask backend and TMM logic
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── /templates             # UI Views
     ├── home.html         # Landing page / Mode selector
     ├── single.html       # Single DBR interface
     └── double.html       # VCSEL Cavity interface
```

## 🎓 Team & Acknowledgements

This tool was developed as part of an academic research and design project.

* **Contributors:**
  * [Kriti Garg - IITD EE'26](https://github.com/Predawnkalery)
  * [Ishaan Lakhotiya - IITD EE'26](https://github.com/Predawnkalery/DBR-Simulation-Suite/tree/main)
* **Supervising Professor:** Prof. [Santanu Manna](https://github.com/Predawnkalery/DBR-Simulation-Suite/tree/main)
* **Institution:** [Department of Electrical Engineering, IIT Delhi](https://github.com/Predawnkalery/DBR-Simulation-Suite/tree/main)

*Special thanks to Mikhail Polyanskiy for maintaining the open-source [RefractiveIndex.INFO database](https://refractiveindex.info/).*

## 📄 License
**All Rights Reserved**

This software is currently proprietary and closed-source. It was developed for internal research and design purposes. Unauthorised copying, distribution, modification, or commercial use of this codebase is strictly prohibited without explicit written permission from the contributing authors and the supervising professor.
