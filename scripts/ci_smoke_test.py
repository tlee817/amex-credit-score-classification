#!/usr/bin/env python3
"""Simple CI smoke test: try importing core dependencies and print versions.

Exit code: 0 on success, non-zero on first import failure.
"""
import importlib
import sys

packages = [
    "pandas",
    "numpy",
    "xgboost",
    "sklearn",
    "joblib",
    "streamlit",
    "plotly",
]

failed = []
for pkg in packages:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", None)
        print(f"import ok: {pkg}", f"(version={ver})" if ver else "")
    except Exception as e:
        print(f"import failed: {pkg}: {e}")
        failed.append((pkg, str(e)))

if failed:
    print("\nSmoke test failed. Packages that failed to import:")
    for pkg, err in failed:
        print(f" - {pkg}: {err}")
    sys.exit(2)

print("\nSmoke test passed: all core imports succeeded")
