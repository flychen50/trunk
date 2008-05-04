#!/usr/bin/env python

# Copyright 2008, Google Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, 
#     this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#  3. Neither the name of Google Inc. nor the names of its contributors may be
#     used to endorse or promote products derived from this software without
#     specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This program demonstrates use of the KML DOM Python SWIG bindings 
# for generating 

import sys
import kmldom

def CreatePointPlacemark(name, lon, lat):
  factory = kmldom.KmlFactory_GetFactory()
  placemark = factory.CreatePlacemark()
  placemark.set_name(name)
  coordinates = factory.CreateCoordinates()
  coordinates.add_point2(lon, lat)
  point = factory.CreatePoint()
  point.set_coordinates(coordinates)
  placemark.set_geometry(point)
  return placemark

def CreateSimple2dLineStringPlacemark(name, lonlat):
  factory = kmldom.KmlFactory_GetFactory()
  placemark = factory.CreatePlacemark()
  placemark.set_name(name)
  coordinates = factory.CreateCoordinates()
  for (lon, lat) in lonlat:
    coordinates.add_point2(lon, lat)
  linestring = factory.CreateLineString()
  linestring.set_tessellate(True)
  linestring.set_coordinates(coordinates)
  placemark.set_geometry(linestring)
  return placemark

def CreateSimple2dPolygonPlacemark(name):
  factory = kmldom.KmlFactory_GetFactory()

  # <outerBoundaryIs><LinearRing>...
  linearing = factory.CreateLinearRing()
  outerboundaryis = factory.CreateOuterBoundaryIs()
  outerboundaryis.set_linearring(linearing)

  # <Polygon><outerBoundaryIs>... <innerBoundaryIs>...
  polygon = factory.CreatePolygon()
  polygon.set_tessellate(True)
  polygon.set_outerboundaryis(outerboundaryis)

  # <Placemark><Polygon>...
  placemark = factory.CreatePlacemark()
  placemark.set_name(name)
  placemark.set_geometry(polygon)

  return placemark

def Create2HolePolygonPlacemark(name):
  factory = kmldom.KmlFactory_GetFactory()

  # <Polygon>
  polygon = factory.CreatePolygon()

  # <outerBoundaryIs><LinearRing><coordinates>
  outerboundaryis = factory.CreateOuterBoundaryIs()
  linearring = factory.CreateLinearRing()
  coordinates = factory.CreateCoordinates()
  coordinates.add_point3(1,2,3)  # XXX
  linearring.set_coordinates(coordinates)
  outerboundaryis.set_linearring(linearring)
  polygon.set_outerboundaryis(outerboundaryis)

  # <innerBoundaryIs><LinearRing><coordinates>
  innerboundaryis = factory.CreateInnerBoundaryIs()
  linearring = factory.CreateLinearRing()
  coordinates = factory.CreateCoordinates()
  coordinates.add_point3(4,5,6)  # XXX
  linearring.set_coordinates(coordinates)
  innerboundaryis.set_linearring(linearring)
  polygon.add_innerboundaryis(innerboundaryis)

  # <innerBoundaryIs><LinearRing><coordinates>
  innerboundaryis = factory.CreateInnerBoundaryIs()
  linearring = factory.CreateLinearRing()
  coordinates = factory.CreateCoordinates()
  coordinates.add_point3(7,8,9)  # XXX
  linearring.set_coordinates(coordinates)
  innerboundaryis.set_linearring(linearring)
  polygon.add_innerboundaryis(innerboundaryis)

  # <Placemark><name>... <Polygon>...
  placemark = factory.CreatePlacemark()
  placemark.set_name(name)
  placemark.set_geometry(polygon)

  return placemark

def main():
  print '== This is %s' % sys.argv[0]

  factory = kmldom.KmlFactory_GetFactory()

  # <Document>
  document = factory.CreateDocument()

  # Each Create*Placemark() creates and returns a Placemark.
  document.add_feature(CreatePointPlacemark('pt0',1,2))
  document.add_feature(CreatePointPlacemark('pt1',3,4))
  lonlat = [(1,2),(3,4),(5,6),(7,8)]
  document.add_feature(CreateSimple2dLineStringPlacemark('line',lonlat))
  document.add_feature(CreateSimple2dPolygonPlacemark('box'))
  document.add_feature(Create2HolePolygonPlacemark('2 holes'))

  # <Placemark><MultiGeometry><Point>... <LineString>...
  placemark = factory.CreatePlacemark()
  multigeometry = factory.CreateMultiGeometry()
  multigeometry.add_geometry(factory.CreatePoint())
  multigeometry.add_geometry(factory.CreateLineString())
  placemark.set_geometry(multigeometry)
  document.add_feature(placemark)

  # <kml>
  kml = factory.CreateKml()
  kml.set_feature(document)

  print 'Serialize to xml...'
  print kmldom.SerializePretty(kml)

  # Release the storage for <kml> and all descendent elements.
  # NOTE: at present this is _required_ to release the storage
  # within the KML DOM.
  factory.DeleteElement(kml)

if __name__ == '__main__':
  main()
