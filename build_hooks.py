import shutil
import os
from pathlib import Path
from subprocess import run as _run
from setuptools import build_meta as _orig

# PEP 517 Required Hooks
prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_sdist = _orig.build_sdist

def get_explicit_conda_urls():
    print("[*] Hook: Fetching explicit conda URLs...")
    res = _run(["conda", "list", "--explicit"], capture_output=True, text=True, shell=True)
    return [line.strip() for line in res.stdout.splitlines() if line.startswith("https://")]

def run_conda_press():
    temp_wheel_dir = Path("portable_wheels")
    if temp_wheel_dir.exists():
        return
        
    temp_wheel_dir.mkdir(exist_ok=True)
    urls = get_explicit_conda_urls()
    
    if urls:
        print("[*] Hook: Starting Conda-to-Wheel conversion...")
        for url in urls:
            pkg_name_raw = url.split('/')[-1]
            base_name = pkg_name_raw.split('-')[0]
            print(f"--- Pressing: {base_name} ---")
            _run(f"conda press --skip-python --fatten {url}", shell=True)

            # Normalization for pip resolver
            for wheel in Path(".").glob(f"{base_name}*.whl"):
                target_path = temp_wheel_dir / f"{base_name}-0.1.0-py3-none-any.whl"
                shutil.move(str(wheel), str(target_path))

def get_requires_for_build_wheel(config_settings=None):
    run_conda_press()
    return _orig.get_requires_for_build_wheel(config_settings)

def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    run_conda_press()
    temp_wheel_dir = Path("portable_wheels")
    try:
        return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
    finally:
        if temp_wheel_dir.exists():
            print(f"[*] Hook: Cleaning up {temp_wheel_dir}...")
            shutil.rmtree(temp_wheel_dir)