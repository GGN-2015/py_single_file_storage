from filelock import SoftFileLock

import os
import json
from typing import Any

class PSFS_Object:
    def __init__(self, filepath:str, timeout:int=-1, encoding:str="utf-8") -> None:
        self.filepath = filepath
        self.timeout = timeout
        self.encoding = encoding

        if not os.path.isfile(filepath):
            raise FileNotFoundError(
                f"filepath '{filepath}' not found.")

        if not filepath.lower().endswith(".py"):
            raise ValueError(
                f"filepath '{filepath}' should endswith '.py'")
        
        self.lockpath = filepath[:-3] + ".lock"
        self.lock_obj = SoftFileLock(
            self.lockpath,self.timeout)
        self.locked:int = 0

    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False

    def acquire(self) -> None:
        if self.locked == 0:
            self.lock_obj.acquire()
        self.locked += 1

    def release(self) -> None:
        self.locked -= 1
        if self.locked == 0:
            self.lock_obj.release()
        elif self.locked < 0:
            self.locked = 0

    def _check_lock(self, func_name:str):
        if not self.locked:
            raise RuntimeError(
                f"You should acquire before {func_name}.")

    def get(self) -> dict[str, Any]:
        self._check_lock("get")
        line_now:str = "{}"

        with open(
            self.filepath, "r", encoding=self.encoding
        ) as fpin:
            for line in fpin:
                if line.strip().startswith("# PSFS_Object:"):
                    line_now = line
                    break
        return json.loads(
            line_now.split(":",maxsplit=1)[-1])

    def remove(self) -> None:
        self._check_lock("remove")
        new_lines:list[str] = []

        # remove PSFS_Object
        with open(
            self.filepath, "r", encoding=self.encoding
        ) as fpin:
            for line in fpin:
                if not line.strip().startswith("# PSFS_Object:"):
                    new_lines.append(line.rstrip("\n"))
        
        while len(new_lines) > 0 and new_lines[-1] == "":
            new_lines.pop()

        # save back
        with open(
            self.filepath, "w", encoding=self.encoding
        ) as fpout:
            fpout.write("\n".join(new_lines))

    def serialize(self, data:dict[str, Any]):
        return json.dumps(
            data,
            ensure_ascii=True,
            separators=(",", ":"),
            indent=None
        )

    def put(self, new_val:dict[str, Any]) -> None:
        self._check_lock("put")
        self.remove()

        with open(
            self.filepath, "a", encoding=self.encoding
        ) as fpout:
            fpout.write(
                f"\n\n# PSFS_Object: {self.serialize(new_val)}\n")
