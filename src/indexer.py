""" Manages indexing into CSV file. Indexer should be structured into {sender:[datetimes]}"""

import configparser
import datetime
import json
import os.path
from typing import List


INIT_PATH = "../backend/init/paths.ini"
STORAGE_PATH = "../backend/init/indexer.json"

class Indexer:

    def __init__(self):

        # Get the filename
        config = configparser.ConfigParser()

        if not os.path.exists(INIT_PATH):
            raise FileNotFoundError(f"No paths.ini file at {INIT_PATH}")

        config.read(INIT_PATH)
        self.resultPath = config.get('PATH', "storage_csv")
        if not self.resultPath:
            raise KeyError("[PATH] storage_csv does not exist in init file.")

        self.indexerPath = STORAGE_PATH
        if not self.indexerPath: # Path is empty
            raise FileNotFoundError("Indexer file is empty. Set STORAGE_PATH")
        elif not os.path.exists(self.indexerPath): # Build a file
            with open(self.indexerPath, "w") as f:
                json.dump({}, f) # Will be an empty json object

        # Now, load the data
        with open(self.indexerPath, "r") as f:
            self.indexer = json.load(f)


    def write_line(self, sender: str, date: datetime.datetime)->List[str]:
        """ Given a line and date, add it to the line.
        :param sender: sender of email
        :param date: datetime object of date
        :return List of all dates"""
        if sender in self.indexer:
            self.indexer[sender].append(date.isoformat())
        else:
            self.indexer[sender] = [date.isoformat()]
            self.update_file()
        return self.read_line(sender)

    # MAYBE
    async def update_file(self):
        """ Simple update to indexer file.
        Why async? This could be heavy, and writing asynchronously may block execution threads"""
        with open(self.indexerPath, "w") as f:
            json.dump(self.indexer, f)

    # Get all datetimes
    def read_line(self, sender: str):
        """ Read a single line of data. Return all dates for this sender. """
        return self.indexer[sender] if sender in self.indexer else []
