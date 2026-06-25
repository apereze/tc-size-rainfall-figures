def main():
    imports = [
        "numpy",
        "pandas",
        "xarray",
        "geopandas",
        "shapely",
        "cartopy",
        "matplotlib",
        "seaborn",
        "cmcrameri",
    ]

    for pkg in imports:
        __import__(pkg)
        print(f"OK: {pkg}")

    print("\nEnvironment is ready.")


if __name__ == "__main__":
    main()
