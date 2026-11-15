import os
import json

class Detector:
    """
    Manages the detection of file modifications.
    
    This class tracks changes in a specified database file and
    records the last modification timestamp.

    :param str option: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, *args, **kwargs):
        """Initializes the Detector class."""
        self.option = "Normal"
        self.db_path = "src/db.json"
        self.modified_path = "src/files/last_modified.json"
        self.modified_time = self.load_modified()

        if len(args) == 1 and args[0] == "Normal":
            self.option = "Normal"
        elif len(args) == 1 and args[0] == "Debug":
            self.option = "Debug"

        self.option = kwargs.get("option" or "opt", self.option)

        if self.option == "Debug":
            print("[DEBUG] Creating a Detector class variable")

    def load_modified(self):
        """
        Loads the last modified timestamp from the stored JSON file.
        
        :returns: The last modification timestamp if available, otherwise None.
        :rtype: float or None
        """
        if os.path.exists(self.modified_path):
            try:
                with open(self.modified_path, 'r') as file:
                    data = json.load(file)
                    return data.get("last_modified", None)
            except Exception as e:
                if self.option == "Debug":
                    print(f"[DEBUG] Error loading timestamp : {e}")
                return None
        return None
    
    def save_modified(self, mtime):
        """
        Saves the last modified timestamp to a JSON file.
        
        :param float mtime: The modification time to be saved.
        """
        try:
            with open(self.modified_path, 'w') as file:
                json.dump({"last_modified": mtime}, file)
        except Exception as e:
            if self.option == "Debug":
                print(f"[DEBUG] Error saving timestamp : {e}")

    def has_db_file_changed(self):
        """
        Checks if the database file has been modified since the last recorded timestamp.
        
        :returns: True if the file has changed or doesn't exist, otherwise False.
        :rtype: bool
        """
        if not os.path.exists(self.db_path):
            return True

        current_mtime = os.path.getmtime(self.db_path)
        if self.modified_time is None or current_mtime != self.modified_time:
            self.modified_time = current_mtime
            self.save_modified(current_mtime)
            return True
        return False