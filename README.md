# Astroscan: A simple control interface for digital cameras

---

### Summary

Astroscan is a simple interactive interface for controlling digital
cameras for doing astronomical imaging, but not only!

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

Default settings should be edited in the config file **config.ini**,
such as the default storage path for captures, flats and bias images,
delay between two successive shots, number of HDR frames and exposure
range in between, etc...

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

The main menu looks like this:

---
![main](/docs/main_menu.png?raw=true)
---

The first entry is the main control interface where you can start taking acquisitions:

---
![capture](/docs/capture_controls.png?raw=true)
---

The second entry goes into another menu allowing you to set on-the-fly various other parameters:

---
![params](/docs/param_menu.png?raw=true)
---

The next entry goes into the "calibration" menu, where you can start
taking flat or bias exposures:

---
![params](/docs/calib_menu.png?raw=true)
---

Have fun!

---