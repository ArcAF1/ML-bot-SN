"""Simple Tkinter GUI for KommunCrawler."""

import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext

from . import run_pipeline


def _run_in_thread(csv_path: str, output_dir: str, log: scrolledtext.ScrolledText) -> None:
    """Execute the pipeline in a background thread and log output."""

    def task() -> None:
        try:
            log.insert(tk.END, "Starting pipeline...\n")
            run_pipeline.run(csv_path, output_dir)
            log.insert(tk.END, "Finished.\n")
        except Exception as exc:  # pragma: no cover - GUI error handling
            log.insert(tk.END, f"Error: {exc}\n")

    threading.Thread(target=task, daemon=True).start()


def main() -> None:
    """Launch the Tkinter GUI."""
    root = tk.Tk()
    root.title("KommunCrawler")

    csv_var = tk.StringVar(value="kommuner.csv")
    out_var = tk.StringVar(value="results")

    tk.Label(root, text="Municipalities CSV:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    csv_entry = tk.Entry(root, textvariable=csv_var, width=40)
    csv_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse...", command=lambda: csv_var.set(
        filedialog.askopenfilename(title="Select CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    )).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    out_entry = tk.Entry(root, textvariable=out_var, width=40)
    out_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse...", command=lambda: out_var.set(
        filedialog.askdirectory(title="Select directory")
    )).grid(row=1, column=2, padx=5, pady=5)

    log = scrolledtext.ScrolledText(root, width=60, height=10)
    log.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    tk.Button(root, text="Run", command=lambda: _run_in_thread(csv_var.get(), out_var.get(), log)).grid(
        row=2, column=0, columnspan=3, pady=10
    )

    root.mainloop()


if __name__ == "__main__":
    main()
