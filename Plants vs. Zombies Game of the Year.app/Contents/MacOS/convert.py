#!/bin/python
import os
import struct
import argparse
import sys


class Userdata:

    def __init__(self, filename, _format=None):
        self.filename = filename
        self.mtime = os.path.getmtime(filename)
        with open(filename, "rb") as f:
            _bytes = f.read()

        self.check_version(_bytes)
        self.num_plant = struct.unpack("<L", _bytes[0x330:0x334])[0]
        self._format = self.guess_format(_bytes) if _format is None else _format
        self.plant_size = 0x58 if self._format == "windows" else 0x3C
        print(f"Input format: {self._format}")
        self.head = _bytes[:0x334]
        self.tail = _bytes[0x334 + self.num_plant * self.plant_size :]
        self.plants = self.load_plants(_bytes)

    def check_version(self, _bytes):
        version = _bytes[0]
        if version != 12:
            raise Exception("Unsupported userdata version {version}")

    def check_zombatar(self, tail):
        num_zombatar = tail[0x2B]
        if len(tail[0x2C + 0x48 * num_zombatar :]) == 0x18:
            return True
        else:
            return False

    def guess_format(self, _bytes):
        tail = _bytes[0x334 + self.num_plant * 0x58 :]
        if len(tail) % 0x48 == 0x44 and self.check_zombatar(tail):
            return "windows"
        tail = _bytes[0x334 + self.num_plant * 0x3C :]
        if len(tail) % 0x48 == 0x44 and self.check_zombatar(tail):
            return "mac"
        raise Exception("Incorrect input format")

    def load_plants(self, _bytes):
        return [_bytes[0x334 + i * self.plant_size : 0x334 + (i + 1) * self.plant_size] for i in range(self.num_plant)]

    def dump(self, _format=None):
        if _format is None:
            _format = "mac" if self._format == "windows" else "windows"
        print(f"Output format: {_format}")

        if self._format == "windows" and _format == "mac":
            plants = [i[:0x14] + i[0x18:0x1C] + i[0x20:0x34] + i[0x38:0x3C] + i[0x40:0x4C] for i in self.plants]
        if self._format == "mac" and _format == "windows":
            zeros = b"\x00\x00\x00\x00"
            plants = [i[:0x14] + zeros + i[0x14:0x18] + zeros + i[0x18:0x2C] + zeros + i[0x2C:0x30] + zeros + i[0x30:] + zeros * 3 for i in self.plants]
        show(plants[0])

        _bytes = self.head + b"".join(plants) + self.tail
        with open(self.filename, "wb") as f:
            f.write(_bytes)
            f.close()
        os.utime(self.filename, (self.mtime, self.mtime))


def show(_bytes):
    for i in range(len(_bytes)):
        print("%02x" % _bytes[i], end="")
        if i % 4 == 3:
            print("|", end="")
        if i % 16 == 15:
            print()
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", "-f", metavar="FORMAT", dest="_from", default=None, help="Source format (windows|mac)")
    parser.add_argument("--to", "-t", metavar="FORMAT", default=None, help="Target format (windows|mac)")
    parser.add_argument("filename", help="Save file (eg: user1.dat)")
    args = parser.parse_args()

    userdata = Userdata(args.filename, _format=args._from)
    userdata.dump(args.to)
