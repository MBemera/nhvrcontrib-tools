#!/usr/bin/env python3
"""Compatibility shim for the install wizard.

Packaging is defined in ``pyproject.toml``. Prefer ``nhvr-setup`` or
``python -m nhvrcontrib.install_wizard`` for the normal user setup flow.
"""

from nhvrcontrib.install_wizard import main

if __name__ == "__main__":
    print("`setup.py` now forwards to the install wizard. Prefer `nhvr-setup` going forward.\n")
    main()
