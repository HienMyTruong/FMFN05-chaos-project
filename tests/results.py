from pathlib import Path
import re
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = DATA_DIR / "test_results"

ENT_LOG = DATA_DIR / "test_ent.log"
PRACTRAND_LOG = DATA_DIR / "test_practrand.log"

RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================
# ENT
# ============================================================

def parse_ent(log_file):
    text = log_file.read_text()

    patterns = {
        "Entropy": r"Entropy\s*=\s*([-\d.]+)",
        "Chi-square": r"Chi square distribution for \d+ samples is\s*([-\d.]+)",
        "Arithmetic mean": r"Arithmetic mean value of data bytes is\s*([-\d.]+)",
        "Monte Carlo Pi": r"Monte Carlo value for Pi is\s*([-\d.]+)",
        "Serial correlation": r"Serial correlation coefficient is\s*([-\d.]+)",
    }

    results = {}

    for name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            results[name] = float(match.group(1))

    return results


def display_ent(results):
    print("\n" + "=" * 60)
    print("ENT RESULTS")
    print("=" * 60)

    for name, value in results.items():
        print(f"{name:25s}: {value}")


def plot_ent(results):
    if not results:
        print("No ENT values found.")
        return

    # ENT values have very different scales, so plot them separately.

    for name, value in results.items():
        plt.figure(figsize=(6, 4))

        plt.bar([name], [value])

        plt.title(f"ENT: {name}")
        plt.ylabel(name)

        plt.tight_layout()

        filename = (
            name.lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        output = RESULTS_DIR / f"ent_{filename}.png"

        plt.savefig(output, dpi=200)
        plt.close()

        print(f"Saved: {output}")


# ============================================================
# PractRand
# ============================================================

def parse_practrand(log_file):
    lines = log_file.read_text().splitlines()

    categories = {
        "normal": 0,
        "unusual": 0,
        "suspicious": 0,
        "very suspicious": 0,
        "fail": 0,
    }

    suspicious_lines = []

    for line in lines:
        lower = line.lower()

        if "fail" in lower:
            categories["fail"] += 1
            suspicious_lines.append(line.strip())

        elif "very suspicious" in lower:
            categories["very suspicious"] += 1
            suspicious_lines.append(line.strip())

        elif "suspicious" in lower:
            categories["suspicious"] += 1
            suspicious_lines.append(line.strip())

        elif "unusual" in lower:
            categories["unusual"] += 1
            suspicious_lines.append(line.strip())

        elif "normal" in lower:
            categories["normal"] += 1

    return categories, suspicious_lines


def display_practrand(categories, suspicious_lines):
    print("\n" + "=" * 60)
    print("PRACTRAND RESULTS")
    print("=" * 60)

    for category, count in categories.items():
        print(f"{category:20s}: {count}")

    if suspicious_lines:
        print("\nPotential problems:")

        for line in suspicious_lines:
            print(f"  {line}")
    else:
        print("\nNo suspicious lines detected.")


def plot_practrand(categories):
    labels = list(categories.keys())
    values = list(categories.values())

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("PractRand result classifications")
    plt.ylabel("Number of occurrences")

    plt.xticks(rotation=25, ha="right")

    plt.tight_layout()

    output = RESULTS_DIR / "practrand_classifications.png"

    plt.savefig(output, dpi=200)
    plt.close()

    print(f"Saved: {output}")


# ============================================================
# Main
# ============================================================

def main():

    print("Randomness test visualizer")

    # ENT
    if ENT_LOG.exists():
        ent_results = parse_ent(ENT_LOG)

        display_ent(ent_results)
        plot_ent(ent_results)

    else:
        print(f"\nENT log not found: {ENT_LOG}")

    # PractRand
    if PRACTRAND_LOG.exists():
        categories, suspicious_lines = parse_practrand(
            PRACTRAND_LOG
        )

        display_practrand(
            categories,
            suspicious_lines
        )

        plot_practrand(categories)

    else:
        print(
            f"\nPractRand log not found: "
            f"{PRACTRAND_LOG}"
        )


if __name__ == "__main__":
    main()