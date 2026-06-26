import sys
from importlib.util import find_spec


REQUIRED_IMPORTS = [
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("xarray", "xarray"),
    ("geopandas", "geopandas"),
    ("shapely", "shapely"),
    ("cartopy", "cartopy"),
    ("matplotlib", "matplotlib"),
    ("seaborn", "seaborn"),
    ("cmcrameri", "cmcrameri"),
    ("cmocean", "cmocean"),
    ("scipy", "scipy"),
    ("statsmodels", "statsmodels"),
    ("sklearn", "scikit-learn"),
    ("pymannkendall", "pymannkendall"),
    ("yaml", "pyyaml"),
    ("netCDF4", "netcdf4"),
    ("cfgrib", "cfgrib"),
]


def main():
    missing = []

    if sys.version_info < (3, 11):
        missing.append("python>=3.11")

    for import_name, package_name in REQUIRED_IMPORTS:
        if find_spec(import_name) is None:
            print(f"MISSING: {package_name}")
            missing.append(package_name)
        else:
            print(f"OK: {package_name}")

    if missing:
        print("\nEnvironment check failed. Missing requirements:")
        for package_name in missing:
            print(f"- {package_name}")
        raise SystemExit(1)

    print("\nEnvironment is ready.")


if __name__ == "__main__":
    main()
