Convert the saves of Plants vs. Zombies between Windows and Mac version
====
__PLEASE BACKUP YOUR SAVES BEFORE USING THIS REPOSITORY.__

__USING ANY CONTENT OF THIS REPOSITORY IS ON YOUR OWN RISK.__

## Usage

* If you installed Plants vs. Zombies via Steam,
	* On Windows, you need to do nothing.
	* On Mac, just run `Plants vs. Zombies Game of the Year.app` in this repository. You may want to copy it to `~/Applications` (not `/Applications`).

* For advanced users,
	* Run `python convert.py user1.dat` to convert the saves between Windows and Mac version.
	* Run `python convert.py -f windows -t mac user1.dat` to convert the saves from Windows to Mac version.
	* Run `python convert.py -f mac -t windows user1.dat` to convert the saves from Mac to Windows version.

## Mechanism

The data format of the plants in the Zen garden is different under Mac and Windows.

For example, the data of a plant on Mac could be:
```
26000000|00000000|00000000|00000000|
00000000|bd33645a|02000000|03000000|
00000000|03000000|00000000|a530635a|
0a695359|00000000|00000000|
```
but on Windows, it should be:
```
26000000|00000000|00000000|00000000|
00000000|00000000|bd33645a|00000000|
02000000|03000000|00000000|03000000|
00000000|00000000|a530635a|00000000|
0a695359|00000000|00000000|00000000|
00000000|00000000|
```

## Known issue

* If your default Python is Python 2, please use `Plants vs. Zombies Game of the Year.app/Contents/MacOS/run2.sh` to replace `Plants vs. Zombies Game of the Year.app/Contents/MacOS/run.sh`.  
And the Python 2 version doesn't support Zombatar.
