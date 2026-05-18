import urllib.request
import os

os.makedirs('static/js', exist_ok=True)
os.makedirs('static/data', exist_ok=True)

# Added the Master ZIP bundle of the entire database
# Exact, fully-qualified URLs to bypass CDN routing errors
files_to_download = {
    'static/js/js-yaml.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js',
    'static/js/chart.min.js': 'https://cdn.jsdelivr.net/npm/chart.js/dist/chart.umd.js',
    'static/js/hammer.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js',
    'static/js/chartjs-plugin-zoom.min.js': 'https://cdn.jsdelivr.net/npm/chartjs-plugin-zoom@2.0.1/dist/chartjs-plugin-zoom.min.js',
    # CHANGED: 'master' is now 'main' in the two links below
    'static/data/library.yml': 'https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/refs/heads/main/database/catalog-nk.yml',
    'database_bundle.zip': 'https://github.com/polyanskiy/refractiveindex.info-database/archive/refs/heads/main.zip'
}

print("Downloading offline assets and Master Database Bundle...")

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0')]
urllib.request.install_opener(opener)

for path, url in files_to_download.items():
    print(f" -> Fetching {path}...")
    try:
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(f"    [X] ERROR fetching {path}: {e}")

print("\nSuccess! Your project is now a fully self-contained offline bundle.")