import os
import zipfile

zf = zipfile.ZipFile("C:\Users\Brendon\Desktop\plugin.video.MyOwnAddon.zip", "w")
for dirname, subdirs, files in os.walk("plugin.video.MyOwnAddon"):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()