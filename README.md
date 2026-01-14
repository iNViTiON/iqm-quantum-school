# IQM Quantum School

This project is a code responsible for [IQM Quantum School](https://www.iqmacademy.com/quantumschool/) designed for **fully reproducible development** using Nix Flakes, [`direnv`](https://direnv.net/), and [`nix-direnv`](https://github.com/nix-community/nix-direnv).  
We recommend using NixOS.

---

## Quick Start (Recommended)

1. [Install Nix](https://nix.dev/install-nix#install-nix) (or [NixOS](https://nixos.org/))
2. [Enable Flakes](https://wiki.nixos.org/wiki/Flakes#Setup)
3. `direnv` and `nix-direnv` on [NixOS](https://wiki.nixos.org/wiki/Direnv#Configuring_on_NixOS) or [Nix](https://nix.dev/guides/recipes/direnv.html)
4. Enter the Project

If this is your first time in the project (or if `.envrc` changes), you **must** run:

```sh
direnv allow
```

Then, enter the directory:

```sh
cd iqm-quantum-school
# direnv will automatically activate the Nix shell
```

You should see:  
`IQM Nix dev shell active`

## Non-Nix
Recommended to use [uv](https://docs.astral.sh/uv/). And I only test with Zed REPL integration.

---

## What You Get

- **Reproducible Python environment**
- **Dev tools:** `uv` + `Python`, `Zed`
- **Automatic shell activation** with `direnv`

## Python Dependencies

All Python dependencies are managed via `pyproject.toml` and locked with `uv.lock`. Just run `uv sync` to install/update dependencies.

---

## How to run


Secrets: this repository already ignores `secret.py`, so the recommended local workflow is to place your token there. Create `secret.py` containing:

```python
IQM_API_TOKEN = "<your-token>"
```

Zed REPL — how to use it (concise)

1. Open the project folder in Zed.
2. Ensure the REPL uses the same interpreter as the project (Nix shell or `.venv`).
3. Open a Python file such as `day1.py`.
4. Open the REPL (command palette) or use the editor's "repl: refresh kernelspecs" command.
5. Move the text cursor to the code block you want to run, then use editor's "repl: run" command.
6. If Zed REPL doesn't found ipython kernel then you might need to setting up the kernel with `uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=project`. Run the "repl: refresh kernelspecs" command again to let editor discover new kernelspecs.

## Package hack
Since there are some packages conflict, we need to manual change a set of package for day 2 and day 3. Please command/uncomment the package in `pyproject.toml` as the comment note before running `uv sync`.
