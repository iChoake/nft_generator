import logging
import os
from json import load

from nft_generator.config import load_config_from_file

# Supported extensions
FILENAME_EXT = ["yaml", "yml", "toml", "json"]

# Default config filenames by priority order
DEFAULT_CONFIG_FILENAME_WITHOUT_EXT = [
    "nftgenerator",
    "NftGenerator",
    "Nftgenerator",
    "generator",
    "Generator",
]
# Use in load_config(filename)
DEFAULT_CONFIG_FILENAME = []

# Fill DEFAULT_CONFIG_FILENAME
for file in DEFAULT_CONFIG_FILENAME_WITHOUT_EXT:
    for ext in FILENAME_EXT:
        DEFAULT_CONFIG_FILENAME.append(file + "." + ext)


def load_config(filename):
    if filename is None: # If the user don't specify the config filename
        for _, _, filenames in os.walk("."):
            for file in filenames: # Search default config in current directory
                if file in DEFAULT_CONFIG_FILENAME:
                    return load_config_from_file(file)
            else: 
                print("Cannot find config file")
                exit()
    else:
        return load_config_from_file(filename) 


def setup_logging(config):
    config = config["general"]["logging"] # get logging config
    logging.basicConfig(
        filename=config.get("filename", "nftgenerator.log"),
        format=config.get("format", "%(name)s:%(levelname)s:%(message)s"),
        level=logging.DEBUG,
    )


def generate(*args, **kwargs):
    # Load config
    config = load_config(kwargs["config"]).parse_config()

    # Setup logging
    setup_logging(config)
    logger = logging.getLogger("nft_generator")
    logger.debug("Logging is ready")  # Check
    logger.info("Starting generate nft")  # Info