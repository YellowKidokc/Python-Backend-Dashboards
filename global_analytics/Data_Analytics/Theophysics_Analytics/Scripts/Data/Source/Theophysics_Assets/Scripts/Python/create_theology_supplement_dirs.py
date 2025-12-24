import os
base = r"D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\COMPLETE_LOGOS_PAPERS_FINAL"
folders = [
    "P01-Logos-Principle",
    "P02-Quantum-Bridge",
    "P03-Algorithm-Reality",
    "P04-Hard-Problem",
    "P05-Soul-Observer",
    "P06-Physics-Principalities",
    "P07-Grace-Function",
    "P08-Stretched-Heavens",
    "P09-Moral-Universe",
    "P10-Creatio-Silico",
    "P11-Protocols-Validation",
    "P12-Decalogue-Cosmos",
]
for f in folders:
    path = os.path.join(base, f)
    os.makedirs(os.path.join(path, "theology"), exist_ok=True)
    if f != "P01-Logos-Principle":
        os.makedirs(os.path.join(path, "supplement"), exist_ok=True)
