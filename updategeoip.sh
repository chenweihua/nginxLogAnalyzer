#!/bin/bash

# Downloads the latest GeoLight DBs from maxmind.
# Updates/replaces the databases that logstash uses.
# These are the IP-to-location databases that logstash uses.
# Maxmind updates them once a month on the first Tuesday of the month.
# See http://dev.maxmind.com/geoip/legacy/geolite/

echo Beginning update of GeoIP databases for logstash.
cd /tmp
rm -f GeoIPASNum.dat.gz GeoIPASNum.dat GeoLiteCity.dat.gz GeoLiteCity.dat
echo Downloading latest files.
wget --quiet --output-document GeoIPASNum.dat.gz http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz || { echo 'Download of GeoIPASNum.dat.gz failed' ; exit 1; }
wget --quiet --output-document GeoLiteCity.dat.gz http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz || { echo 'Download of GeoLiteCity.dat.gz failed' ; exit 1; }

echo Unzipping
gunzip GeoIPASNum.dat.gz
gunzip GeoLiteCity.dat.gz

echo Setting permissions
chmod 664 GeoIPASNum.dat GeoLiteCity.dat
chown logstash:logstash GeoIPASNum.dat GeoLiteCity.dat

echo Replacing existing files and backing up the old.
cd /opt/logstash/vendor/geoip/
mv -f GeoIPASNum.dat GeoIPASNum.dat.bak && mv /tmp/GeoIPASNum.dat .
mv -f GeoLiteCity.dat GeoLiteCity.dat.bak && mv /tmp/GeoLiteCity.dat .

echo Restarting logstash
# Modify for your distro services model.
service logstash restart

echo Done


