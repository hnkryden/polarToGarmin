# Converts Polar data to garmin

The python code has the following steps.
1. Login to polar-account and fetch activity data
2. Removes the tags "Creator" and "Author" that prevents polar .tcx to be imported to garmin.
3. Writes the .tcx files that can be imported to Garmin

Note: There are also free online tools for the convertion, such as http://polar2garm.in and http://polarconverter.com

### Usage: 

```console
$ python converter.py
Polar username: 
Password:
```
