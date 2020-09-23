# QGIS visualization workshop
 2020 QGIS visualization workshop

Author: Topi Tjukanov, [Gispo Ltd.](https://www.gispo.fi/en/home/) 

Parts of this blog post are based on [my blog post](https://www.gispo.fi/en/open-software/geogiffery-in-2020-with-qgis-temporal-controller/) about the QGIS Temporal Controller and visualization methods. 

The workshop was first held in September 2020 and it aims to cover many different tips and tricks for QGIS visualization in versions 3.14 onwards. After this workshop participants should be able to:
- Import shared visualization resources (e.g. palettes, styles) to QGIS
- Have a good understanding of how expressions work in QGIS and how they can be used in data-driven visualizations
- How to make animated maps using QGIS either with Temporal Controller or PyQGIS

## Prerequisites
Workshop is designed to work with QGIS 3.14.15 or newer. You can download latest QGIS version [here](https://qgis.org/en/site/forusers/download.html). 

Basic knowledge on using QGIS and working with spatial data helps. 

# Workshop 
## Introduction to cartography trick & tips in QGIS
What makes a beautiful map and an informative visualization? The answer is not straightforward and especially trying to cover both aspects on a single map can be very difficult. 

At the other end of the scale with spatial visualizations are the rustic old artistic maps whereas in the other end are the polished and clean dashboards. Trying to replicate the look and feel of old maps with modern tools is much more difficult than the latter. 

![An example of classic cartography. Source: https://timomeriluoto.kapsi.fi/Sivut/Paasivu/KARTAT/Teemakartat/Teemakartat.html](https://github.com/GispoCoding/QGIS-visualization-workshop/blob/master/images/old_map_example.PNG?raw=true)

Randomness can be inserted to QGIS visualizations easily with expressions which will be covered in this workshop later. So a bit of *noise* in your maps can make them look very different and more personal.

Few general tips for visualizing 
1.  Don’t add unnecessary elements on your map. Even ditch (or at least simplify) the background map if you can. Don’t forget that you can change your project background color and black is  **always**  cool.
2.  Experiment with colors and blending modes. Just like with any static map, these really give that extra touch to your outputs.Choosing the right colors is a key factor in making stunning cartography. An excellent resource to help you with that is [this blog post](https://blog.datawrapper.de/beautifulcolors/) by Datawrapper. 
3.  Use expressions and dynamic styling. We will cover those later. 

## Importing visualization resources
Most of the resources QGIS uses for visualization is XML-based or text based. This means that exporting and importing data is relatively easy. First add layer from the data folder to your QGIS project (e.g. the countries dataset)

I have shared some of my QGIS resources to a [separate repository. ](https://github.com/tjukanovt/qgis_styles)

![You can import style files directly from an URL to your Style Manager.](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/import_style.PNG)

*Try to import a few styles from [Klas Karlsson's awesome collection](http://qgis-hub.fast-page.org/styles.php?i=1) and apply those to your layers.* 

## Introduction to QGIS expressions
Expressions in QGIS are "SQL'ish" way to select, filter and process data. It is extremely powerful way not only to do basic data operations but also to use in visualization. 

Basic expression dialog you will see all around the software looks like this:

![Expression dialog can be found from QGIS in several places](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/expression_dialog.PNG)

The **Function List** inside expressions contains functions as well as fields and values loaded from your data. In the **Expression** window you see the calculation expressions you create with the **Function List**. For the most commonly used operators, see **Operators**.

*Browse through the functions list. Do you have an idea what those could be used for? Check out the Aggregate category. Can you think of an use case for those?*

Add a layer from the data folder and open the layer symbolody from properties. Then change the style to **Geometry Generator** and try the following expression to create lines from polygons:

    make_line(point_n( oriented_bbox(  $geometry  ),2), 
       point_n( oriented_bbox(  $geometry  ),3))

*What kind of results do you get?*   

An example of a bit longer expression with few QGIS extra flavors can be seen in the [Qlimt style](https://gist.github.com/tjukanovt/c0f00116f88fb0a1e102e0485e9aa6dc) and the geometry generator expression. 
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

Try adding the **finland_municipalities.geojson** file from the data folder to your project and create a geometry generator style for it and paste the expression above to the layer. Try editing the style and see how the shapes change. 

## QGIS Temporal Controller
From the version 3.14 onwards QGIS has had a functionality to visualize temporal data better called Temporal Controller. 

You need to acquire a vector dataset with some information about time and preferably in a valid way. In QGIS the basic valid datetime format is  _YYYY-MM-DD hh:mm:ss,_ but the Temporal Controller can work also only with date information (e.g. .  _YYYY-MM-DD)._ Read more about different types to represent date and time from my  [old blog post](https://medium.com/@tjukanov/geogiffery-in-a-nutshell-introduction-to-qgis-time-manager-31bb79f2af19).

The data folder contains a shapefile with all the buildings in the Helsinki region called region_buildings.shp. 

Temporal Controller configuration offers you the following options:

-   Fixed time range. Here you can manually select when ALL the features of the layer will be drawn on the map. This option doesn’t require the data to have any date or time fields. Could be helpful e.g. with a background layer in your animation.
-   Single field with Date/Time. This option only requires one attribute and set the event duration manually for all features. See more below.
-   Separate Fields for Start and End Date/Time. Your data should have two attributes with start and end times. Individual features that interact with the maps temporal extent will be rendered. 
-   Separate Fields for Start and Event Duration. Like the ones above, this also works on individual features, but event duration should be read from the data. 
-   Start and End Date/Time from Expressions. If your data does not have a valid datetime column you can use this option to make one form existing fields. 
- Redraw Layer Only. Like the first option, but layer gets redrawn on every frame. The first option and this are probably the biggest changes compared to the Time Manager plugin. This basically allows you to redraw layers even without a temporal attribute. You can for example use random values here that change on every frame or parse out seconds from. You can get some crazy ideas by applying the ideas from [this presentation by Nyall Dawson.](http://www.youtube.com/watch?v=v8li0VdrDBI)


![Adding temporal data to your project and turning on the tempral capabilities](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/add_temporal_data.PNG)

After this you need to activate the Temroral Controller panel in your project (the clock icon) and turn on the animated view (the freen button). The animated view allows you to browse back and forth with the building data and see how the region has developed. 

![Helsinki city center in 1912 with the temporal view](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/temporal_view.PNG)

If there was also a dataset with demolished buildings this could be even more informative and interesting. This could be exported in to an animated gif or a video. If you want to add some basemaps to your QGIS, check out [this script.](https://raw.githubusercontent.com/klakar/QGIS_resources/master/collections/Geosupportsystem/python/qgis_basemaps.py) 

*Try to visualize the buildings in an informative way. What kind of information is important when building this type of animaton?*

## Creating a dashboard with QGIS
Dashboards seem to be a thing currently in data visualization. So let's try to build one using QGIS. First thing a dashboard needs is data that is updating on regular basis. In this example we will use ship locations form the [Digitraffic API](https://www.digitraffic.fi/en/marine-traffic/#/restjson--api). 

QGIS can read an API that returns valid GeoJSON directly from an URL without needing to save it to disk first. You can try that out by opening up the Data Source Manager and pasting this layer in there: 
https://meri.digitraffic.fi/api/v1/locations/latest

![You can insert a GeoJSON directy from an URL](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/insert_geojson.PNG)

This should load a GeoJSON layer to your project in a few seconds. In the data we are interested in the following attributes:
- mmsi: ship identification number
- sog: speed over ground
- cog: course over ground
- timestampExternal: an epoch timestamp

The API also returns some really old features, so you can first filter those out from the screen by adding a filter to the layer with a nice round epoch:

    "timestampExternal">1600800000000

Even better way is to do the filtering already in the query, so try adding the following layer to your project:

    https://meri.digitraffic.fi/api/v1/locations/latest?from=1600800000000|layername=OGRGeoJSON

First thing you need to do for a real dashboard look is to set the project background color to black. You can do this 

    2 + ("sog"/20)

To rotate the symbols we can use another attribute from the data. Open the marker dialog from the ship layer and find the rotation definition. Open again the expression dialog from the small black arrow and enter the following expression as the value:

     "cog" 



![Use your visualization skills to create an informative dashboard](https://raw.githubusercontent.com/GispoCoding/QGIS-visualization-workshop/master/images/dashboard_sample.PNG)

As a last step, to make the data update automatically, we can use PyQGIS to reload the source on regular intervals. See the example below ([Big thanks to Keith Jenkins!](https://twitter.com/kgjenkins/status/1308495702843154440?s=20)):

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


This scipt updates a layer based on the name. So first we have to rename the ship layer to ship_autoUpdate. Leave it running and admire your dashboard. For the ultimate look you should press CTRL + Shift + Tab to enter map only mode.

## Conclusions
This repository is work in progress. It was first created in September 2020 and the idea is to iterate the contents further in later workshops. PR's and issues (e.g. on content proposals) are welcome!