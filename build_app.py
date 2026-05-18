import os
import shutil
import PyInstaller.__main__

# 1. FORCE PYTHON TO PROVE IT HAS THE LIBRARY
try:
    import flaskwebgui
    print(f" SUCCESS: Found flaskwebgui at: {flaskwebgui.__file__}")
except ImportError:
    print(" ERROR: Python cannot find flaskwebgui in this environment!")
    print("Run this exact command first: python -m pip install flaskwebgui")
    exit(1)

# 2. CLEANUP OLD CACHE
print(" Cleaning up old build files...")
for folder in ['build', 'dist']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
if os.path.exists('DBR_Simulator.spec'):
    os.remove('DBR_Simulator.spec')

# 3. RUN COMPILER FROM INSIDE PYTHON
print(" Compiling application...")
PyInstaller.__main__.run([
    'desktop_app.py',
    '--name=DBR_Simulator',
    '--noconsole',
    # '--hidden-import=flaskwebgui',
    '--hidden-import=refractiveindex',
    '--add-data=templates:templates',
    '--add-data=static:static',
    '--add-data=database_bundle.zip:.',
    # Notice we REMOVED the formulas.yml and lab_materials.yml flags
    '--noconfirm'
])

print(" Build Complete! Check the 'dist' folder.")
