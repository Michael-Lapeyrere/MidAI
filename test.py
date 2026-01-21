import os
import django
from pathlib import Path
from collections import defaultdict

# ⚠️ IMPORTANT : mettre ton settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MidAI.settings")
django.setup()

from django.conf import settings
from django.apps import apps

# Dictionnaire pour stocker les fichiers par chemin relatif
files_map = defaultdict(list)

# 1️⃣ Parcours des dossiers dans STATICFILES_DIRS
for static_dir in settings.STATICFILES_DIRS:
    static_dir = Path(static_dir)
    for root, _, files in os.walk(static_dir):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), static_dir)
            files_map[rel_path].append(os.path.join(root, f))

# 2️⃣ Parcours des dossiers static/ des apps
for app_config in apps.get_app_configs():
    app_static = Path(app_config.path) / "static"
    if app_static.exists():
        for root, _, files in os.walk(app_static):
            for f in files:
                rel_path = os.path.relpath(os.path.join(root, f), app_static)
                files_map[rel_path].append(os.path.join(root, f))

# 3️⃣ Affiche uniquement les doublons
print("⚠️ Fichiers statiques en conflit (mêmes chemins relatifs) :")
found = False
for rel_path, paths in files_map.items():
    if len(paths) > 1:
        found = True
        print(f"\nChemin relatif : {rel_path}")
        for p in paths:
            print(f" - {p}")

if not found:
    print("✅ Aucun doublon trouvé, tout est unique !")
