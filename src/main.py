"""
PerfLens entry point.
"""

from src.app.application import Application


def main() -> None:

    application = Application()

    application.initialize()

    application.run()


if __name__ == "__main__":
    main()