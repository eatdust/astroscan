#!/usr/bin/python
import cursesmenu as cm
import curtsies as ci
from curtsies.fmtfuncs import *
import scanner as sc
import time as time
import sys as sys
import threading as th
#check async

#storage path for output scans
toppath = '/home/chris/' + 'chateaurenard/'
imgpath = toppath + 'raws/'
flatpath = toppath + 'flats/'
zeropath = toppath + 'zeros/'

#img settings
imgroot = 'test'
imgtype = 'nef'
imglgth = 6
hdrlgth = 2

#hdr default settings
hdrframe = 1
exprange = 2

#global image positionning counter
imgcount = 0
imginfty = 1000

#global value recording motor states
forward = True
energize = False
scanning = False

#delay between two image scan (in sec)
mindelay = 0
maxdelay = 30




def main():


    camera = sc.scanner(pylog=True, summary=False)
    time.sleep(2)
    
    menu = cm.CursesMenu("Astroscan", "Actions")
    scanitem = cm.items.FunctionItem("Capture controls",scan_controls,[camera,menu])
    
    settingmenu = cm.SelectionMenu(strings=[],title="Astroscan parameters menu")
    
    resetitem = cm.items.FunctionItem("Set image count",reset_imgcount,[])
    hdritem = cm.items.FunctionItem("Set HDR number",reset_hdrframe,[])
    inftyitem = cm.items.FunctionItem("Set maximum count",reset_imginfty,[])
    rangeitem = cm.items.FunctionItem("Set exposure bracket",reset_exprange,[])
    expitem = cm.items.FunctionItem("Set exposure time",reset_exptime,[camera])
    isoitem = cm.items.FunctionItem("Set ISO value",reset_iso,[camera])

    calibmenu = cm.SelectionMenu(strings=[],title="Astroscan calibration menu")
    flatitem = cm.items.FunctionItem("Take flat exposures",take_flats,[camera,0.0])
    zeroitem = cm.items.FunctionItem("Take zero exposures",take_zeros,[camera,0.0])
    
    menu.append_item(scanitem)
    
    settingmenu.append_item(resetitem)
    settingmenu.append_item(hdritem)
    settingmenu.append_item(inftyitem)
    settingmenu.append_item(rangeitem)
    settingmenu.append_item(expitem)
    settingmenu.append_item(isoitem)
    
    
    settingitem = cm.items.SubmenuItem("Settings menu",settingmenu,menu)
    menu.append_item(settingitem)
    
    calibmenu.append_item(flatitem)
    calibmenu.append_item(zeroitem)

    calibitem = cm.items.SubmenuItem("Calibration menu",calibmenu,menu)
    menu.append_item(calibitem)

    menu.show()





def reset_imgcount():

    global imgcount

    imgcount = int( input('imgcount = '))

    print('Global image counter reset to: ',imgcount)
    time.sleep(3)

    
    return


def reset_hdrframe():

    global hdrframe

    hdrframe = int( input('hdrframe = '))

    print('Number of bracketting frames set to: ',hdrframe)
    time.sleep(3)
    
    return


def reset_imginfty():

    global imginfty

    imginfty = int( input('imginfty = '))

    print('Maximal image count reset to: ',imginfty)
    time.sleep(3)

    
    return



def reset_exprange():

    global exprange

    exprange = int( input('exprange = '))

    print('Exposure bracketting increment set to: ',exprange)
    time.sleep(3)
    
    return


def reset_exptime(camera):

    expchoice = int( input('expchoice (see ghoto2) = '))

    camera.connect()

    expvalue = camera.set_exposure_time(expchoice)

    print('Exposure time set to: ',expvalue)
    time.sleep(3)

    camera.deconnect()
    
    return



def reset_iso(camera):

    isochoice = int( input('isochoice (see ghoto2) = '))

    camera.connect()

    isovalue = camera.set_iso(isochoice)

    print('ISO value set to: ',isovalue)
    time.sleep(3)

    camera.deconnect()
    
    return




def scan_frames(camera,delay,stopscan):

    global imgcount
    global hdrframe
    global exprange
    global scanning
    
    if hdrframe <=0:
        print('scan_frames: hdrframe <=0!')
        return

    if exprange <=0:
        print('scan_frames: exprange <=0!')
        return

    success = True
    
    camera.connect()
    
    nullExpChoice, nullExpValue = camera.get_exposure_time()
    
    while not stopscan.is_set():

        stgcount = str(imgcount).zfill(imglgth)

        hdrcount = 0

        for ihdr in range(-int(hdrframe/2),int(hdrframe/2)+1):

            expChoice = int(nullExpChoice + ihdr* exprange)
            expValue = camera.set_exposure_time(expChoice)

            
            stghdr = str(hdrcount).zfill(hdrlgth)
            
            imgname = imgroot + '_' + stgcount +'_' + stghdr + '.' + imgtype

            print('capturing: ',imgname+'                 ')
            print('exposure: ',expValue+'               ')
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            camera.single_capture(imgpath,imgname,success)

            hdrcount+=1
            

        if not success:
            print('scan_frames: ABORT, capturing failure!')
            stopscan.set()
            scanning = False
            return
            
        imgcount+=1

        if imgcount > imginfty:
            print('scan_frames: ABORT, max imgcount reached= ',imgcount)
            stopscan.set()
            scanning = False            
            return
        
        

#wait after motor move        
        time.sleep(delay)
        

    nullExpValue = camera.set_exposure_time(nullExpChoice)
    camera.deconnect()

    return



def take_flats(camera,delay):

    nflats = int( input('nflats = '))

    success = True
    
    camera.connect(success)

    if not success:
        print('take_flats: cannot connect!')
        return
    
    for count in range(0,nflats):

        stgcount = str(count).zfill(imglgth)
            
        imgname = imgroot + '_flat_' + stgcount + '.' + imgtype

        print('scanning: ',imgname+'                 ')
        sys.stdout.write("\033[F")

        camera.single_capture(flatpath,imgname)            

#wait if needed
        time.sleep(delay)

    camera.deconnect(success)

    if not success:
        print('take_flats: cannot disconnect!')
    
    return



def take_zeros(camera,delay):

    nzeros = int( input('nzeros = '))

    success = True

    camera.connect(success)

    if not success:
        print('take_flats: cannot connect!')
        return
    
    nullExpChoice, nullExpValue = camera.get_exposure_time()    
    
    expvalue = camera.set_exposure_time(0)
    print('Exposure time set to: ',expvalue)
    time.sleep(3)

    
    for count in range(0,nzeros):

        stgcount = str(count).zfill(imglgth)
            
        imgname = imgroot + '_zero_' + stgcount + '.' + imgtype

        print('scanning: ',imgname+'                 ')
        sys.stdout.write("\033[F")

        camera.single_capture(zeropath,imgname)            

#wait if needed
        time.sleep(delay)
        

    nullExpValue = camera.set_exposure_time(nullExpChoice)
    print()
    print('Exposure time reset to: ',nullExpValue)
    time.sleep(3)

        
    camera.deconnect(success)

    if not success:
        print('take_flats: cannot disconnect!')
    
    return








def scan_controls(camera,menu):

    global imgcount
    global hdrframe
    global exprange
    global energize
    global forward
    global scanning
    
    menu.pause()

    delay = mindelay
    stopscan = th.Event()
    stopscan.clear()
    
    izero = 5
    iss = 3 + izero
    isd = 5 + izero
    isc = 7 + izero
    isr = 9 + izero
    iim = 11 + izero
    ihd = 13 + izero
    
    with ci.FullscreenWindow() as window:
        with ci.Input() as inputgen:
            scr = ci.FSArray(window.height, window.width)

            ilast = window.height 

            scr[izero-1,0:window.width-1] = ci.fsarray([u'_'*window.width])
            scr[ilast-1,0:window.width-2] = ci.fsarray([u'_'*window.width])
            scr[ilast-2,0:window.width-2] = ci.fsarray([u'_'*window.width])
            
            msg = ci.fmtstr(on_blue(bold(yellow(u'CONTROL INTERFACE'))))
            center = int((window.width-msg.width)/2)
            scr[izero, center:msg.width] = [msg]

            msgspeed = ci.fmtstr(u'delay:    ')
            scr[iss, 0:msgspeed.width] = [msgspeed]
            ispeed = msgspeed.width+1
            
            msgcw = ci.fmtstr(u'direction:')
            scr[isd, 0:msgcw.width] = [msgcw]
            icw = msgcw.width+2
            msgfwd = ci.fmtstr('FORWARD ')
            msgback = ci.fmtstr('BACKWARD')

            msgamp = ci.fmtstr(u'position:')
            scr[isc, 0:msgamp.width] = [msgamp]
            msgampon = ci.fmtstr(bold(green('LOCKED  ')))
            msgampoff = ci.fmtstr(bold(yellow('UNLOCKED')))
            
            msgrun = ci.fmtstr(u'state:')
            scr[isr, 0:msgrun.width] = [msgrun]
            msgon = ci.fmtstr(bold(green('SCANNING')))
            msgoff = ci.fmtstr(bold(red('STOP    ')))

            msgimg = ci.fmtstr(u'imgcount: ')
            scr[iim, 0:msgimg.width] = [msgimg]
            imgstg=ci.fmtstr(str(imgcount).zfill(imglgth))
            scr[iim,icw:icw+imgstg.width] = [imgstg]
            
            delaylab=ci.fmtstr(on_blue(bold(yellow('delay (s) ='))))
            delaystg=ci.fmtstr(on_blue(red(bold(' '+str(int(delay))))))
            scr[izero,0:delaylab.width]=[delaylab]
            scr[izero,delaylab.width:delaylab.width+delaystg.width+1]=[delaystg]

            isolab=ci.fmtstr(on_blue(bold(yellow('iso ='))))
            if camera.error == 0:
                isostg=ci.fmtstr(on_blue(red(bold(' '+str(camera.get_iso())))))
            else:
                isostg = ci.fmtstr(on_blue(red(bold(' '+'No Cam'))))
            scr[izero,window.width-isolab.width-isostg.width
                :window.width-isostg.width]=[isolab]
            scr[izero,window.width-isostg.width:window.width]=[isostg]

            shutlab=ci.fmtstr(on_blue(bold(yellow('exptime ='))))

            if camera.error == 0:
                shutstg=ci.fmtstr(on_blue(red(bold(' '+str(camera.get_exposure_time())))))
            else:
                shutstg = ci.fmtstr(on_blue(red(bold(' '+'No Cam'))))

            icenter=int((window.width+shutlab.width+shutstg.width)/2)
            scr[ilast-2,icenter-shutlab.width-shutstg.width:icenter-shutstg.width]=[shutlab]
            scr[ilast-2,icenter-shutstg.width:icenter]=[shutstg]




            hdrlab=ci.fmtstr(on_blue(bold(yellow('hdrframe ='))))
            hdrstg=ci.fmtstr(on_blue(red(bold(' '+str(hdrframe)))))
            scr[ilast-2,window.width-hdrlab.width-hdrstg.width
                :window.width-hdrstg.width]=[hdrlab]
            scr[ilast-2,window.width-hdrstg.width:window.width]=[hdrstg]

            explab=ci.fmtstr(on_blue(bold(yellow('exprange ='))))
            expstg=ci.fmtstr(on_blue(red(bold(' '+str(exprange)))))
            scr[ilast-2,0:explab.width]=[explab]
            scr[ilast-2,explab.width:explab.width+expstg.width+1]=[expstg]
            

            scanning = False

            if not scanning:
                scr[isr,icw:icw+msgoff.width] = [msgoff]
            else:
                scr[isr,icw:icw+msgon.width] = [msgon]
                
            if forward:
                scr[isd,icw:icw+msgfwd.width] = [msgfwd]
            else:
                scr[isd,icw:icw+msgback.width] = [msgback]

            if energize:
                scr[isc,icw:icw+msgampon.width] = [msgampon]
            else:
                scr[isc,icw:icw+msgampoff.width] = [msgampoff]


#displays initial values
                
            window.render_to_terminal(scr)
            
            for c in inputgen:
                if c == '<ESC>':
                    if scanning:
                        stopscan.set()
                        thscan.join(timeout=None)
                        scanning = False
                    break

                elif c == '<UP>':
                    ispeed = max(ispeed + 1,msgspeed.width+1)
                    ispeed = min(ispeed,window.width-1)
                    scr[iss,ispeed:ispeed+1] = [ci.fmtstr(yellow('|'))]
                    delay = int(mindelay + float(ispeed-msgspeed.width-1)/float(
                        window.width-msgspeed.width-2)*(maxdelay-mindelay))

                elif c == '<DOWN>':
                    scr[iss,ispeed:ispeed+1] = [ci.fmtstr(u' ')]
                    ispeed = max(ispeed - 1,msgspeed.width+1)
                    ispeed = min(ispeed,window.width-1)
                    delay = int(mindelay + float(ispeed-msgspeed.width-1)/float(
                        window.width-msgspeed.width-2)*(maxdelay-mindelay))

                elif c == '<RIGHT>':
                    if not scanning:
                        if not forward:
                            forward = True
                        scr[isd,icw:icw+msgfwd.width] = [msgfwd]

                elif c == '<LEFT>':
                    if not scanning:
                        if forward:
                            forward = False
                        scr[isd,icw:icw+msgback.width] = [msgback]

                elif c == '<SPACE>':
                    scanning = not(scanning)
                    if scanning:
                        stopscan.clear()
                        thscan = th.Thread(name='scan',
                                           target=scan_frames,
                                           args=[camera,delay,
                                                 stopscan])
                        thscan.start()
                        scr[isr,icw:icw+msgon.width] = [msgon]
                    else:                        
                        stopscan.set()
                        thscan.join(timeout=None)
                        scr[isr,icw:icw+msgoff.width] = [msgoff]

                   
                elif c == '<Ctrl-j>':
                    energize = not(energize)
                    if energize:
                        scr[isc,icw:icw+msgampon.width] = [msgampon]
                    else:
                        scr[isc,icw:icw+msgampoff.width] = [msgampoff]

                else:
                    msghelp = ci.fmtstr(bold(yellow(
                        u'Use enter, arrow keys and space bar for control. Escape to exit')))
                    centerhelp = int((window.width-msghelp.width)/2)
                    scr[ilast-1,centerhelp:centerhelp+msghelp.width] = [msghelp]

#display updated values                    


#                delaylab=ci.fmtstr(on_blue(bold(yellow('delay ='))))
                delaystg=ci.fmtstr(on_blue(red(bold(' '+str(int(delay))))))
                scr[izero,0:delaylab.width]=[delaylab]
                scr[izero,delaylab.width:delaylab.width+delaystg.width+1]=[delaystg]

                imgstg=ci.fmtstr(str(imgcount).zfill(imglgth))
                scr[iim,icw:icw+imgstg.width] = [imgstg]

                
                window.render_to_terminal(scr)

    menu.resume()
    return





if __name__ == "__main__":
    main()
