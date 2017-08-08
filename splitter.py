"""
Requires Pillow (PIL)

This program is easiest to use if you have Microsoft Dual Monitor tools.
You dont have to use it, but it lets you determine the pixel positioning of
your monitors. You can also trial and error calibrate this, or find it other
ways.

This app was designed for dual screens of roughly the same size, but
different resilutions.

You can also just set pairs of the split images as your backgrounds,
but then you cant have a slideshow running (need individual images)

I made my measurements in the correct system of measurement, by inches should
work just fine too (i hope).

Remember to set the wallpapers to tile (sanity check)

* I might add in the ability to account for the bezels/gap between monitors in
  the future.
_______________________________________________________________________________
         ________________
      ^  |                |  ______________         } Vertical offset, V
      |  |    left mon    | |   right mon  |  ^
  H1  |  |    R1H & R1W   | |   R2H & R2W  |  | H2
      |  |                | |______________|  v
      v  |________________|
                            <------W2------>
         <--------W1------>
_______________________________________________________________________________
STEPS
1. measure physical positions of your Monitors
2. check resolutions of Monitors
3. input parameters below, and save.
4. Create a parent folder where you want to work. Then create three child
   folders called 'input', 'dual' and 'output' and place slicer.py at the same
   at that level. Place the photos you want to convert into 'input'.
   eg;
        parent >    dual       >
                    output     >
                    slicer.py
                    input      >    ultrawidewallpaper1.png
                                    ultrawidewallpaper2.png
                                    ultrawidewallpaper1.jpg
                                            etc...
5. run slicer.py after installing Pillow/PIL and image_slicer.
6. set location of displays in 'Display settings' (right click desktop)
    -set the right screen to be at: R1H*(1-(H2/H1)). This value will be printed
     out for you after filling in the input parameters. NOTE THAT 0 IS LOCATED
     AT THE TOP OF THE SCREEN. REFERENCE POINT IS TOP.
    -you can 'fine tune' by editing a registry key
        -the reg key is at
        -HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Configuration\
            -edit Position.cy for the right screen (in the example case)
            - The multiple display configs listed here are memories of you
              swapping out other monitors. IF you cant tell which one is the
              current set up, delete all the subfolders here (the one in
              Configuration with the crazy names), sign out, sign back in, and
              a just the current active config file will be regenerated. edit
              position.cy. you can tell which screen is which by reading the
              data column. Sign out/in again.
"""
import glob, os
import tkinter as tk
from PIL import Image

##############  INPUT PARAMETERS  ###################
H1 = 34 #height of first (left) monitor
H2 = 29 #width of first (left) monitor

W1 = 62 #height of second (right) monitor
W2 = 52 #width of second (right) monitorV

R1W = 3840#horizontal resolution of first monitor
R1H = 2160 #vertical resolution of first monitor

R2W = 1920#horizontal resolution of second monitor
R2H = 1080#vertical resolution of second monitor

V = 1.5 #vertical offset between tops of monitors.
#lower = input('is the left or right monitor lower? (left1/right0): ')
#mainmon = input('which is the main monitor? (left1/right0): ') #want to add an option to base the stretch options off of this mon.

#H = input('input horizontal gap between monitors(cm). Enter 0 if the image was designed for dual monitors rather than an ultrawide monitor: ')
H = 0 #distance between monitors
def find_max_height(R1H,R2H,M1H,M2H,H1,H2):
    print((M1H,M2H))
    if R2H+M2H > R1H:
        return(R2H+M2H) #if the monitors are diagonal, this should take the max
    if R1H+M1H > R2H:
        return(R1H+M1H) #if the monitors are diagonal, this should take the max
    else:
        return(int(max([R1H,R2H])))
def monitor_placement(V,H1,H2,R1H,R2H,lower):
    if lower == 0:
        M2H = R1H*((1.0*V/H1)) #the pixel height that monitor 2 should be at.
        print('monitor 2 should be placed at: '+str(int(M2H)))
        M1H = 0
    elif lower ==  1:
        M1H = R2H*((1.0*V/H2)) #the pixel height that monitor 2 should be at.
        print('monitor 1 should be placed at: '+str(int(M1H)))
        M2H = 0
    return((int(M1H),int(M2H)))

#flag1 = str(input('maintain PPI (yes1/no0)? : '))
def main(H1,H2,W1,W2,R1W,R1H,R2W,R2H,V,H,lower,mainmon,centresplit, PPI,gap):
    print((H1,H2,W1,W2,R1W,R1H,R2W,R2H,V,H,lower,mainmon,centresplit, PPI,gap))
    ######################################################
    #centresplit = input('force split in centre? (yes1/no0): ')
    (M1H,M2H) = monitor_placement(V,H1,H2,R1H,R2H,lower)
    i = 1
    for file0 in glob.glob("./splitterinput/*.*"): #this is the folder where you put the pictures you want to adapt for dual screens.
        if file0[-4:] == '.png' or file0[-4:] == '.jpg' :
            print('now processing: '+str(file0))
            width = R1W+R2W #input widths of a proper image generated from MS DualWallpaper
                         #this should be the width of your two monitors combined (pixels)
            height = find_max_height(R1H, R2H, M1H, M2H,H1,H2) #height of your tallest monitor. If your monitors are offset,
                                              # This could be improved
                          # then it should be the total height of both monitors, minus the overlap.
            print(height)
            new_im = Image.new('RGB', (width, height))

            picture = Image.open(file0)
            #image 1
            x1_offset = 0 #shouldnt need to change this
            y1_offset = M1H #change this if left monitor is lower than right
                         # DMT (dual monitor tools) by MS can tell you what the
                         # offsets should be. DMT>>Monitors>>working
            if mainmon == 1:
                left    = 0
            elif mainmon ==0:
                left = 0 # i make this more flexible in the future
            bottom  = picture.size[1]
            if centresplit == 1:
                right   = picture.size[0]/2 #force image split in middle
            else:
                right = picture.size[0]*W1/(W1+W2) #proportional split
            top     = 0
            leftim = picture.crop(( left , top , right , bottom ))  #resolution of left screen
            leftim = leftim.resize((R1W,R1H), Image.ANTIALIAS)
            new_im.paste(leftim, (x1_offset,y1_offset))

            #image 2
            picture2 = Image.open(file0)
            x2_offset = int(leftim.size[0]) #place next to left im
            y2_offset = int(M2H) #relative position of the monitors

            toplevel    = int(picture2.size[1]*V/H1)
            bottomlevel = int(picture2.size[1]*(V+H2)/H1)


            if gap == 1:
                left    = picture.size[0]*W1/(W1+W2) + int(1.0*width*H/(W1+W2))
            elif gap ==0:
                left    = picture2.size[0]/2 #+ int(1.0*width*H/(W1+W2))#crop off whats on the left screen

            bottom  = bottomlevel
            if PPI == 1:
                right = left + W2*picture2.size[0]/(2*W1)
            else:
                right = picture2.size[0]


            top     = toplevel
            rightim = picture2.crop(( left , top , right , bottom ))  #resolution of left screen
            #rightim = rightim.resize((R1W,R1H), Image.ANTIALIAS)

            rightim = rightim.resize((R2W,R2H), Image.ANTIALIAS)

            new_im.paste(rightim, (x2_offset,y2_offset))

            new_im.save('./output/'+file0[16:], quality =100)
            print(str(i) + ' images complete')
            i +=1
        else: #the file is not a jpg or png
            print('file '+file0+' is not a .png or .jpg. Skipping...')
            continue
#main(H1,H2,W1,W2,R1W,R1H,R2W,R2H,V,H,lower,mainmon)
