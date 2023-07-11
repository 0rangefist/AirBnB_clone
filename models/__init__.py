#!/usr/bin/python3
""" init for the models package """
from models.engine.file_storage import FileStorage

# create a FileStorage instance
storage = FileStorage()

# reload to memory any objects that have been saved to file
storage.reload()
