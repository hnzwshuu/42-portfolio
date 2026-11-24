import importlib
import sys


REQUIRED_PACKAGES: dict[str, str] = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def load_package(name: str) -> object | None:
    try:
        return importlib.import_module(name)
    except ImportError:
        return None


def package_version(module: object) -> str:
    version = getattr(module, "__version__", "unknown")
    return str(version)


def check_dependencies() -> dict[str, object]:
    loaded: dict[str, object] = {}

    print("Checking dependencies:")
    for package, message in REQUIRED_PACKAGES.items():
        module = load_package(package)
        if module is None:
            print(f"[MISSING] {package} - install this package to continue")
        else:
            loaded[package] = module
            print(f"[OK] {package} ({package_version(module)}) - {message}")

    return loaded


def print_install_instructions() -> None:
    print()
    print("Some programs could not be loaded.")
    print("Install dependencies with pip:")
    print("pip install -r requirements.txt")
    print()
    print("Or install dependencies with Poetry:")
    print("poetry install")
    print("poetry run python loading.py")


def print_dependency_management_comparison() -> None:
    print()
    print("Dependency management comparison:")
    print("pip uses requirements.txt as a direct package list.")
    print("Poetry uses pyproject.toml and a lock file")
    print("for reproducible projects.")


def build_matrix_data(numpy_module: object, pandas_module: object) -> object:
    np = numpy_module
    pd = pandas_module

    generator = np.random.default_rng(seed=42)  # type: ignore[attr-defined]
    signal_strength = generator.normal(loc=75.0, scale=12.0, size=1000)
    anomaly_score = generator.normal(loc=0.0, scale=1.0, size=1000)
    latency_ms = generator.gamma(shape=2.0, scale=18.0, size=1000)

    return pd.DataFrame(  # type: ignore[attr-defined]
        {
            "signal_strength": signal_strength,
            "anomaly_score": anomaly_score,
            "latency_ms": latency_ms,
            "is_glitch": anomaly_score > 1.75,
        }
    )


def save_visualization(data_frame: object, matplotlib_module: object) -> str:
    matplotlib_module.use("Agg")  # type: ignore[attr-defined]
    pyplot = importlib.import_module("matplotlib.pyplot")

    output_path = "matrix_analysis.png"
    figure, axes = pyplot.subplots(1, 2, figsize=(10, 4))

    axes[0].hist(
        data_frame["signal_strength"],  # type: ignore[attr-defined, index]
        bins=30,
        color="#198754",
    )

    axes[0].set_title("Signal Strength")
    axes[0].set_xlabel("Strength")
    axes[0].set_ylabel("Count")

    axes[1].scatter(
        data_frame["latency_ms"],  # type: ignore[attr-defined, index]
        data_frame["anomaly_score"],  # type: ignore[attr-defined, index]
        c=data_frame["is_glitch"],  # type: ignore[attr-defined, index]
        cmap="coolwarm",
        alpha=0.7,
    )
    axes[1].set_title("Latency vs Anomaly")
    axes[1].set_xlabel("Latency (ms)")
    axes[1].set_ylabel("Anomaly Score")

    figure.tight_layout()
    figure.savefig(output_path)
    pyplot.close(figure)

    return output_path


def main() -> int:
    print()
    print("LOADING STATUS: Loading programs...")
    print()
    loaded = check_dependencies()

    if set(REQUIRED_PACKAGES) != set(loaded):
        print_install_instructions()
        print_dependency_management_comparison()
        return 1

    print()
    print("Analyzing Matrix data...")
    data_frame = build_matrix_data(loaded["numpy"], loaded["pandas"])
    print("Processing "
          f"{len(data_frame)} data points...")  # type: ignore[arg-type]

    print("Generating visualization...")
    output_path = save_visualization(data_frame, loaded["matplotlib"])
    print(f"Results saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
