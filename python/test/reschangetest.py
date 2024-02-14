import subprocess
import time

''' Must be a multiple of 8!! '''
n = 712

m = 1232
framerate = 61

mode = f'{n}x{m}_{framerate}.00'
cvt_data = f'{n} {m} {framerate}'


print(mode)
print(cvt_data)
try:
    output = subprocess.check_output('xrandr -s ' + mode, shell=True)
except:

    print('Resolution Does Not Exist!! Adding new Resolution')
    output = subprocess.check_output(f'cvt {cvt_data}'.encode('utf-8'), shell=True)
    output = output.decode('utf-8')

    modeline = output.split('\n')[1]
    modeline = modeline[(modeline.index('ine')+4):(len(modeline))]
    print(modeline)

    output = subprocess.check_output('xrandr --newmode ' + modeline, shell=True)
    output = output.decode('utf-8')

    output = subprocess.check_output('xrandr --addmode HDMI-1 ' + mode, shell=True)
    output = output.decode('utf-8')

    output = subprocess.check_output('xrandr -s ' + mode, shell=True)
    output = output.decode('utf-8')

time.sleep(5)

output = subprocess.check_output('xrandr -s 1600x1200 -r 60', shell=True)
output = output.decode('utf-8')



