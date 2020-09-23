# QGIS visualization workshop
 2020 QGIS visualization workshop

Author: Topi Tjukanov

## Goals

After this workshop participants should be able to:
- Import shared visualization resources (e.g. palettes, styles) to QGIS
- Have a good understanding of how expressions work in QGIS and how they can be used in data-driven visualizations
- How to make animated maps with QGIS either with Temporal Controller or PyQGIS

## Prerequisites
Workshop is designed to work with QGIS 3.14.15 or newer. You can download latest QGIS version [here](https://qgis.org/en/site/forusers/download.html). 

The content assumes you have basic knowledge on using QGIS and working with spatial data. 

# Workshop exercises
## Basic cartography trick & tips in QGIS


Trying to replicate the look and feel of old maps with modern tools is more difficult than one would imagine. 
![An example of classic cartography. Source: https://timomeriluoto.kapsi.fi/Sivut/Paasivu/KARTAT/Teemakartat/Teemakartat.html](https://github.com/GispoCoding/QGIS-visualization-workshop/blob/master/images/old_map_example.PNG?raw=true)

So a bit of *noise* in your maps can make them look very different and more personal, 

Choosing the right colors is a key factor in making stunning cartography. An excellent resource to help you with that is [this blog post](https://blog.datawrapper.de/beautifulcolors/) by Datawrapper. 

## Importing visualization resources
Most of the resources QGIS uses for visualization is XML-based or text based. This means that exporting and importing data is relatively easy. 

I have shared some of my QGIS resources to a [separate repository. ](https://github.com/tjukanovt/qgis_styles)

![You can import style files directly from an URL to your Style Manager.](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/import_style.PNG)


## Introduction to QGIS expressions
Expressions in QGIS are "SQL'ish" way to select, filter and process data. 

![Expression dialog can be found from QGIS in several places](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/expression_dialog.PNG)

The **Function List** inside expressions contains functions as well as fields and values loaded from your data. In the **Expression** window you see the calculation expressions you create with the **Function List**. For the most commonly used operators, see **Operators**.

An example of a bit longer expression with few QGIS extra flavors can be seen in the Qlimt style and the geometry generator expression. 
```
with_variable('my_geom',
CASE WHEN 
 num_geometries( $geometry)>1
 THEN 
   geometry_n(  $geometry,  @geometry_part_num)
  ELSE
    $geometry
  END,
  with_variable('shape',rand(1,4),
  CASE WHEN 
  @shape =1
  THEN 
  minimal_circle( @my_geom )
  WHEN
  @shape =2
  THEN
  oriented_bbox( @my_geom )
  WHEN
  @shape =3
  THEN
  oriented_bbox( @my_geom )
  WHEN
  @shape =4
  THEN
   simplify(@my_geom, rand(1,20))
  END))
  ```

Note when writing expressions that fields name should be double-quoted. Values or string should be simple-quoted.

Expresisons 

## QGIS Temporal Controller

Temporal Controller configuration offers you the following options:

-   Fixed time range. Here you can manually select when ALL the features of the layer will be drawn on the map. This option doesn’t require the data to have any date or time fields. Could be helpful e.g. with a background layer in your animation.
    
-   Single field with Date/Time. This option only requires one attribute and set the event duration manually for all features. See more below.
-   Separate Fields for Start and End Date/Time. Your data should have two attributes with start and end times. Individual features that interact with the maps temporal extent will be rendered. An example of this type of data could be building vectors which would have building date and demolition date.
-   Separate Fields for Start and Event Duration. Like the ones above, this also works on individual features, but event duration should be read from the data. As an example if you are working with the meteorite data, you could build event durations based on the magnitude of the meteorite to build a nice visual effect. So bigger meteorites stay on the map for a longer time.
-   Start and End Date/Time from Expressions. If your data does not have a valid datetime column you can use this option to make one form existing fields. For instance if you are using the region_buildings dataset in your animation provided to you earlier, you could build a valid timestamp using the expression to_date(“YYYYMMDD”) as the starting date and for example to_date(‘2020-01-01’) as the end date to make the buildings appear cumulatively.
- Redraw Layer Only. Like the first option, but layer gets redrawn on every frame. The first option and this are probably the biggest changes compared to Time Manager. This basically allows you to redraw layers even without a temporal attribute. You can for example use random values here that change on every frame or parse out seconds from. You can get some crazy ideas by applying the ideas from [this presentation by Nyall Dawson.](http://www.youtube.com/watch?v=v8li0VdrDBI)

## Creating a DASHBOARD with QGIS
Dashboards seem to be a thing. So let's build one using QGIS.

First thing a dashboard needs is live data.

    "timestampExternal">1600800000000

To make the data update automatically, we can use PyQGIS to reload the source on regular intervals. See this example.

    import threading
    import datetime
    import re
    
    def autoUpdateLayers():
      t = threading.Timer(15.0, autoUpdateLayers)
      t.start()
      for layer in QgsProject.instance().mapLayers().values():
        if 'autoUpdate' in layer.name():
          print('autoUpdating layer: '+layer.name())
          layer.dataProvider().forceReload()
          layer.setName(
            re.sub(
              'autoUpdate.*',
              'autoUpdated ' + datetime.datetime.now().strftime('%c'),
              layer.name()
            )
          )
        if 'cancel' in layer.name():
          print('stopping execution')
          t.cancel()
    
    
    autoUpdateLayers()
