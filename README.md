Convert the saves of Plants vs. Zombies between Windows and Mac version
====
__PLEASE BACKUP YOUR SAVES BEFORE USING THIS REPOSITORY.__

__USING ANY CONTENT OF THIS REPOSITORY IS ON YOUR OWN RISK.__

## Usage

* If you installed Plants vs. Zombies via Steam,
	* On Windows, you need to do nothing.
	* On Mac, just run `Plants vs. Zombies Game of the Year.app` in this repository. You may want to copy it to `~/Applications` (not `/Applications`).

* For advanced users,
	* Run `python convert.py mac user1.dat` to convert the saves from Windows to Mac version.
	* Run `python convert.py windows user1.dat` to convert the saves from Mac to Windows version.

## Known issue

* Doesn't support Zombatar.
* If your default Python is Python 3, please use `Plants vs. Zombies Game of the Year.app/Contents/MacOS/convert3.py` to replace `Plants vs. Zombies Game of the Year.app/Contents/MacOS/convert.py`.
