from flask import Flask, request, jsonify, render_template
import numpy as np
import cmath
import yaml
import os
import sys
import zipfile
import shutil
import urllib.request

import sys

# --- SAFE LOGGER ---
def safe_print(message):
    try:
        # Only attempt to print if stdout hasn't been detached by PyInstaller
        if sys.stdout is not None:
            print(message)
            # Force the terminal to render the text immediately (bypass Waitress buffering)
            sys.stdout.flush() 
    except Exception:
        pass # Silently ignore the print if the console is hidden




# --- PATH RESOLUTION ---
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    exe_dir = os.path.dirname(sys.executable)
    if sys.platform == 'darwin' and exe_dir.endswith('MacOS'):
        EXTERNAL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(exe_dir)))
    else:
        EXTERNAL_DIR = exe_dir
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXTERNAL_DIR = BASE_DIR

# --- FLASK APP INITIALIZATION ---
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

# --- AUTO-UPDATER FOR LAB DATA ---
formulas_path = os.path.join(EXTERNAL_DIR, 'formulas.yml')
lab_db_path = os.path.join(EXTERNAL_DIR, 'lab_materials.yml')

import traceback

# --- GLOBAL ERROR HANDLER ---
@app.errorhandler(Exception)
def handle_global_error(e):
    # Grab the exact line of code and technical reason it crashed
    error_trace = traceback.format_exc()
    
    # Print it to the background terminal just in case
    print(f"\n[CRITICAL BACKEND ERROR]:\n{error_trace}\n")
    
    # Send a clean JSON package to the frontend so it doesn't just say "Failed to fetch"
    return jsonify({
        "status": "error",
        "message": f"An unexpected system error occurred: {str(e)}",
        "traceback": error_trace # This gives you the technical data if they report it
    }), 500

def sync_with_github():
    print("🔄 Checking GitHub for updated lab materials...")
    # repo_url_base = "https://raw.githubusercontent.com/Predawnkalery/DBR-Simulation-Suite/offline/"
    repo_url_base = "https://raw.githubusercontent.com/Predawnkalery/DBR-Simulation/refs/heads/main/"
    try:
        urllib.request.urlretrieve(repo_url_base + "formulas.yml", formulas_path)
        urllib.request.urlretrieve(repo_url_base + "lab_materials.yml", lab_db_path)
        print("✅ Lab materials synced successfully.")
    except Exception as e:
        print(f"⚠️ Offline or sync failed. Using local materials. ({e})")

# COMMENT OUT THIS LINE TO DISABLE THE INTERNET CHECK AND ALWAYS USE LOCAL FILES (EVEN IF OUTDATED)
sync_with_github()

# --- LOAD LAB DATABASES ---
try:
    with open(formulas_path, 'r') as f:
        LAB_FORMULAS = yaml.safe_load(f) or {}
    with open(lab_db_path, 'r') as f:
        LAB_DATABASE = yaml.safe_load(f).get('materials', [])
except Exception as e:
    print(f"Notice: Lab databases not found. ({e})")
    LAB_FORMULAS = {}
    LAB_DATABASE = []

# --- LIBRARY SETUP ---
USE_MOCK = False
try:
    from refractiveindex import RefractiveIndexMaterial
except ImportError:
    print("Library 'refractiveindex' not installed. Using Mock mode.")
    USE_MOCK = True

try:
    from custom_db import LabMaterial
except ImportError:
    print("Warning: custom_db.py not found. Lab materials won't work.")

class MockMaterial:
    def __init__(self, shelf, book, page):
        self.name = f"{book} - {page} (MOCK)"
    def get_refractive_index(self, w): return 1.55
    def get_extinction_coefficient(self, w): return 0.001

# --- ROUTES ---
@app.route('/')
def home(): return render_template('home.html')
@app.route('/single')
def single_dbr(): return render_template('single.html')
@app.route('/double')
def double_dbr(): return render_template('double.html')

# --- NEW ROUTE: SERVE LAB CATALOG TO FRONTEND ---
@app.route('/lab_catalog')
def get_lab_catalog():
    if not LAB_DATABASE:
        return jsonify({})
    
    # Organize flat lab database into Book (Groups) and Pages (Materials)
    books = {}
    for idx, mat in enumerate(LAB_DATABASE):
        group = mat.get('group', 'Uncategorized Lab Data')
        if group not in books:
            books[group] = []
        books[group].append({
            'PAGE': str(idx), # We use the index as the "Page" ID!
            'name': mat.get('name', f"Sample {idx}")
        })
    
    book_list = []
    for group_name, pages in books.items():
        book_list.append({'BOOK': group_name, 'name': group_name, 'content': pages})

    # Package it into a single "Shelf"
    lab_shelf = {
        'SHELF': 'in_house',
        'name': '🏠 In-House Lab Data',
        'content': book_list
    }
    return jsonify(lab_shelf)

# --- 2. CORE TMM ENGINE ---

def build_single_dbr(periods, mat_high, mat_low, mat_sub, mat_air, lambda_c):
    nh = float(mat_high['n']) + 1j * float(mat_high['k'])
    nl = float(mat_low['n'])  + 1j * float(mat_low['k'])
    ns = float(mat_sub['n'])  + 1j * float(mat_sub['k'])
    na = float(mat_air['n'])  + 1j * float(mat_air['k'])

    n_list = [na]
    d_list = [0]
    layer_profile = [{"label": "Air", "n": na.real, "d": 0}]

    for _ in range(periods):
        n_list.extend([nh, nl])
        d_h = lambda_c / (4 * mat_high['n'])
        d_l = lambda_c / (4 * mat_low['n'])
        d_list.extend([d_h, d_l])
        
        # USE ACTUAL MATERIAL NAMES FOR THE VISUALIZER
        layer_profile.append({"label": mat_high['name'], "n": nh.real, "d": d_h * 1e9})
        layer_profile.append({"label": mat_low['name'], "n": nl.real, "d": d_l * 1e9})

    n_list.append(ns)
    d_list.append(0)
    layer_profile.append({"label": f"Substrate ({mat_sub['name']})", "n": ns.real, "d": 0})

    return n_list, d_list, layer_profile

def build_vcsel(top_p, bot_p, mat_high, mat_low, mat_cav, mat_sub, mat_air, lambda_c):
    nh = float(mat_high['n']) + 1j * float(mat_high['k'])
    nl = float(mat_low['n'])  + 1j * float(mat_low['k'])
    nc = float(mat_cav['n'])  + 1j * float(mat_cav['k'])
    ns = float(mat_sub['n'])  + 1j * float(mat_sub['k'])
    na = float(mat_air['n'])  + 1j * float(mat_air['k'])

    n_list = [na]
    d_list = [0]
    layer_profile = [{"label": "Air", "n": na.real, "d": 0}]

    # Top Mirror
    for _ in range(top_p):
        n_list.extend([nh, nl])
        d_h = lambda_c / (4 * mat_high['n'])
        d_l = lambda_c / (4 * mat_low['n'])
        d_list.extend([d_h, d_l])
        layer_profile.append({"label": mat_high['name'], "n": nh.real, "d": d_h * 1e9})
        layer_profile.append({"label": mat_low['name'], "n": nl.real, "d": d_l * 1e9})

    # Cavity
    n_list.append(nc)
    d_c = lambda_c / mat_cav['n']
    d_list.append(d_c) 
    layer_profile.append({"label": f"Cavity ({mat_cav['name']})", "n": nc.real, "d": d_c * 1e9})

    # Bottom Mirror
    for _ in range(bot_p):
        n_list.extend([nl, nh])
        d_l = lambda_c / (4 * mat_low['n'])
        d_h = lambda_c / (4 * mat_high['n'])
        d_list.extend([d_l, d_h])
        layer_profile.append({"label": mat_low['name'], "n": nl.real, "d": d_l * 1e9})
        layer_profile.append({"label": mat_high['name'], "n": nh.real, "d": d_h * 1e9})

    # Substrate
    n_list.append(ns)
    d_list.append(0)
    layer_profile.append({"label": f"Substrate ({mat_sub['name']})", "n": ns.real, "d": 0})

    return n_list, d_list, layer_profile

def calculate_tmm(n_list, d_list, wavelengths):
    R = []
    for wl in wavelengths:
        k0 = 2 * np.pi / wl
        M = np.identity(2, dtype=complex)
        num_layers = len(n_list)
        for i in range(num_layers - 1):
            n1 = n_list[i]
            n2 = n_list[i+1]
            D = np.array([
                [(n2 + n1) / (2 * n1), (n2 - n1) / (2 * n1)],
                [(n2 - n1) / (2 * n1), (n2 + n1) / (2 * n1)]
            ], dtype=complex)
            M = np.dot(M, D)
            if i < (num_layers - 2):
                phi = k0 * n2 * d_list[i+1]
                P = np.array([[np.exp(1j * phi), 0], [0, np.exp(-1j * phi)]], dtype=complex)
                M = np.dot(M, P)
        r_coeff = M[1, 0] / M[0, 0]
        R.append(float(abs(r_coeff)**2))
    return R

# --- 3. HELPER (UPDATED FOR LAB DATA) ---
def get_material_data(mat_data, wavelength):
    if not mat_data or not mat_data.get('page'): return None
    try:
        shelf = mat_data['shelf']
        
        # 1. Check if it is an In-House Material
        if shelf == 'in_house':
            mat_idx = int(mat_data['page']) # We stored the index in the page variable
            yaml_node = LAB_DATABASE[mat_idx]
            mat = LabMaterial(yaml_node, LAB_FORMULAS)
            name = mat.name
            
        # 2. Otherwise, use public RefractiveIndex database
        else:
            book, page = mat_data['book'], mat_data['page']
            if not USE_MOCK:
                safe_print(f"Fetching material from RefractiveIndex database:{shelf} - {book} - {page}")
                mat = RefractiveIndexMaterial(shelf, book, page)
            else:
                mat = MockMaterial(shelf, book, page)
            name = f"{book}-{page}"
        safe_print(f"Calculate optical properties for {name} at {wavelength} nm")
        # Calculate optical properties
        n = float(mat.get_refractive_index(wavelength))
        try: k = float(mat.get_extinction_coefficient(wavelength))
        except: k = 0.0
    
        if n > 0: t = wavelength / (4 * n)
        else: t = 0
        safe_print(f"Calculated optical properties for {name} at {wavelength} nm -> n: {n}, k: {k}, t: {t} m")
        return {"name": name, "n": n, "k": k, "t": t}
    except Exception as e:
        return {"error": str(e)}
# --- 4. MAIN PROCESSOR ---
@app.route('/process', methods=['POST'])
def process_selection():
    data = request.json
    
    try:
        center_wl_nm = float(data.get('wavelength', 600))
        center_wl_m = center_wl_nm * 1e-9 
        mode = data.get('mode', 'single')
        action = data.get('action', 'both')
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid input."})
    
    mat1 = get_material_data(data.get('mat1'), center_wl_nm)
    mat2 = get_material_data(data.get('mat2'), center_wl_nm)
    sub  = get_material_data(data.get('substrate'), center_wl_nm)
    cav  = get_material_data(data.get('cavity'), center_wl_nm) if mode == 'double' else None

    materials_to_check = {'Material 1': mat1, 'Material 2': mat2, 'Substrate': sub}
    if mode == 'double': materials_to_check['Cavity'] = cav

    for name, mat in materials_to_check.items():
        if not mat: return jsonify({"status": "error", "message": f"Missing {name}."})
        if 'error' in mat: return jsonify({"status": "error", "message": f"Data error for {name}: {mat['error']}"})

    start_wl = center_wl_m - 1000e-9
    end_wl = center_wl_m + 1000e-9
    wavelengths = np.linspace(start_wl, end_wl, 1500)
    air_props = {'n': 1.0, 'k': 0.0}

    try:
        # ALWAYS build the layer structure so the frontend can draw it
        if mode == 'single':
            layers = int(data.get('layers', 10))
            n_list, d_list, layer_profile = build_single_dbr(layers, mat1, mat2, sub, air_props, center_wl_m)
        elif mode == 'double':
            top_p = int(data.get('layers_top', 10))
            bot_p = int(data.get('layers_bot', 10))
            n_list, d_list, layer_profile = build_vcsel(top_p, bot_p, mat1, mat2, cav, sub, air_props, center_wl_m)

        # Base response package (includes the visual profile)
        response_data = {
            "status": "success",
            "mat1": mat1,
            "mat2": mat2,
            "substrate": sub,
            "layer_profile": layer_profile
        }
        if mode == 'double': response_data["cavity"] = cav

        # Only run the heavy matrix math if we are actually simulating
        # In server.py, update the process_selection route:
        if action in ['simulate', 'both']:
            reflectivity = calculate_tmm(n_list, d_list, wavelengths)
            # Sanitize NaN and Infinity to 0.0 or 1.0
            safe_reflectivity = np.nan_to_num(reflectivity, nan=0.0, posinf=1.0, neginf=0.0)
            response_data["plot_x"] = (wavelengths * 1e9).tolist()
            response_data["plot_y"] = safe_reflectivity.tolist()

    except Exception as e:
        return jsonify({"status": "error", "message": f"Simulation failed: {str(e)}"})
        
    return jsonify(response_data)

if __name__ == '__main__':
    print("Server running. Go to http://127.0.0.1:5000")
    app.run(debug=True, port=5000)