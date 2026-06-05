# PyInstaller bundle entry point — delegates to the real entry in gui/entry.py
# (handles --run headless mode vs. launching the GUI, sets up the browser env).
from gui.entry import main

if __name__ == "__main__":
    main()
