import sys
import os
import shutil

def resource_path(relative_path):
    """ Get absolute path to resource for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # Extracted folder in PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_db_path():
    """Returns path to a writable DB: AppData in exe, local in dev"""
    if getattr(sys, 'frozen', False):
        # AppData path for EXE users
        base_dir = os.path.join(os.path.expanduser("~"), "FitnessAppData")
        os.makedirs(base_dir, exist_ok=True)
        db_path = os.path.join(base_dir, "gym_management.db")

        # If DB not already copied, copy from bundled location
        if not os.path.exists(db_path):
            try:
                bundled_db = os.path.join(sys._MEIPASS, "database", "gym_management.db")
                if os.path.exists(bundled_db):
                    shutil.copy(bundled_db, db_path)
            except Exception as e:
                print("Error copying bundled DB:", e)
        return db_path

    else:
        # Raw run uses local project path
        return os.path.abspath("database/gym_management.db")
