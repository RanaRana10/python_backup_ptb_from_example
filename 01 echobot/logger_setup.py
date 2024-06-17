import logging

# Set up RANA NAME logger
rana_logger = logging.getLogger("RANA NAME")
rana_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("FILE is:%(asctime)s ---Name is %(name)s -- ***%(levelname)s*** - %(message)s")
file_handler = logging.FileHandler("0logfile.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
rana_logger.addHandler(file_handler)
rana_logger.propagate = False

# Set up RICO TERMINAL logger
rico_logger = logging.getLogger("RICO TERMINAL")
rico_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("CONSOLE is:%(asctime)s ---Name is %(name)s -- ***%(levelname)s*** - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
rico_logger.addHandler(console_handler)
rico_logger.propagate = False
