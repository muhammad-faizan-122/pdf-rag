import logging


def setup_logger(fn="logs/app.log"):
    """Setup logger for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler(fn), logging.StreamHandler()],
    )
