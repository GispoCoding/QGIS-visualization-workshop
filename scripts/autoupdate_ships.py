import threading
import datetime
import re

class updateThreading:
    def __init__(self) -> None:
        self.t = None
    def autoUpdateLayers(self):
        self.t = threading.Timer(15.0, self.autoUpdateLayers)
        self.t .start()
        for layer in QgsProject.instance().mapLayers().values():
            if 'autoUpdate' in layer.name():
                print('autoUpdating layer: '+layer.name())
                layer.dataProvider().forceReload()
                layer.setName(
                    re.sub(
                        'autoUpdate.*',
                        'autoUpdated ' + datetime.datetime.now().strftime("%H:%M:%S"),
                        layer.name()
                    )
                )
            if 'cancel' in layer.name():
                print('stopping execution')
                self.t .cancel()
                
updateThreading().autoUpdateLayers()