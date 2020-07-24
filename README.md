# Astroscan: A simple control interface for digital cameras

---

### Summary

Astroscan is a simple interactive interface for controlling digital
cameras while doing astronomy.

Please ensure that you have a working installation of
[gphoto2](https://github.com/gphoto/gphoto2) as well as
[python-gphoto2](https://github.com/jim-easterbrook/python-gphoto2). Astroscan
also relies on [curses-menu](https://github.com/pmbarrett314/curses-menu) and
[curtsies](https://github.com/bpython/curtsies).

### Astroscan window

Astroscan should be started within a **xterm**. It is assumed that a
digital camera is plugged in (via USB), on, and **astroscan** will
first attempt to initialize it. If no camera is connected,
**astroscan** will proceed with a warning message and would only allow
to explore the menus (pretty useless then!).

The main file (astroscan.py) should certainly be edited to set the
default storage path for captures, flats and bias images.

```python

#storage path for captures
toppath ='/tmp/tests/'
imgpath = toppath + 'raws/'
flatpath = toppath + 'flats/'
zeropath = toppath + 'zeros/'

#img settings
imgroot = 'test'
imgtype = 'nef'

#hdr default settings
hdrframe = 1
exprange = 2

```
---
