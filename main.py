# Copyright (c) 2025 devgagan : https://github.com/devgaganin
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
from shared_client import start_client


async def load_and_run_plugins() -> None:
    """Load all plugins from the plugins directory and run them asynchronously."""
    await start_client()
    plugin_dir = "plugins"
    if not os.path.exists(plugin_dir):
        print(f"Plugin directory '{plugin_dir}' does not exist.")
        return

    plugins = [
        f[:-3] for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        try:
            module = importlib.import_module(f"plugins.{plugin}")
            func = getattr(module, f"run_{plugin}_plugin", None)
            if func is None:
                print(f"No entry function found for plugin '{plugin}', skipping.")
                continue

            print(f"Running plugin '{plugin}'...")
            await func()

        except Exception as e:
            print(f"Error running plugin '{plugin}': {e}")


async def main() -> None:
    """Main async entry point."""
    await load_and_run_plugins()
    # Keep the script running (useful for bots or persistent services)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Starting clients ...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Unhandled exception: {e}")
        sys.exit(1)
