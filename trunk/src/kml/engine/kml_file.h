// Copyright 2008, Google Inc. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without 
// modification, are permitted provided that the following conditions are met:
//
//  1. Redistributions of source code must retain the above copyright notice, 
//     this list of conditions and the following disclaimer.
//  2. Redistributions in binary form must reproduce the above copyright notice,
//     this list of conditions and the following disclaimer in the documentation
//     and/or other materials provided with the distribution.
//  3. Neither the name of Google Inc. nor the names of its contributors may be
//     used to endorse or promote products derived from this software without
//     specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
// WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
// EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
// OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// This file contains the declaration of the KmlFile class.

#ifndef KML_ENGINE_KML_FILE_H__
#define KML_ENGINE_KML_FILE_H__

#include <string>
#include "boost/scoped_ptr.hpp"
#include "kml/dom.h"
#include "kml/engine/kmz_file.h"
#include "kml/engine/object_id_parser_observer.h"
#include "kml/engine/shared_style_parser_observer.h"
#include "kml/base/util.h"

namespace kmlengine {

const char kDefaultXmlns[] = "http://www.opengis.net/kml/2.2";
const char kDefaultEncoding[] = "utf-8";

// The KmlFile class represents the instance of a KML file from a given URL.
class KmlFile {
 public:
  // This creates a KmlFile from a memory buffer of either KML or KMZ data.
  // In the case of Kmz the KmzFile module's ReadKml() is used to read the
  // KML data from the KMZ archive.  On any parse errors NULL is returned
  // and a human readable error message is saved in the supplied string.
  // The caller is responsible for deleting the KmlFile this creates.
  static KmlFile* CreateFromParse(const std::string& kml_or_kmz_data,
                                  std::string *errors);

  // This public constructor permits use creation of an empty KmlFile.
  KmlFile();

  // This parses the KML in the given input buffer.  The encoding from the XML
  // header is saved if such exists.  The default XML namespace and any
  // namespace prefix definitions found in the root element are also saved.
  // The root element of the parse is returned.  All Objects with ids are
  // saved in a map for use with GetObjectById.  Any use of this method
  // clears the internal state of the instance of this class.  If an errors
  // string is supplied any parse errors are stored there.  On any parse
  // error including duplicate id a NULL is returned.
  const kmldom::ElementPtr& ParseFromString(const std::string& kml,
                                            std::string* errors);

  // This returns the root element of this KML file.  The initial state of
  // this is NULL.  A parse failure also sets this to NULL>
  const kmldom::ElementPtr& root() const {
    return root_;
  }

  // This serializes the KML from the root.  The xmlns() value is added to
  // the root element, the set of namespace prefixes to namespaces is added,
  // and the encoding is set in a prepended XML header:
  //    <?xml version="1.0" encoding="ENCODING">
  //    <kml xmlns="XMLNS" xmlns:PREFIX1="XMLNS1" xmlns:PREFIX2="XMLNS2"...>
  //    ...
  //    </kml>
  bool SerializeToString(std::string* xml_output) const;

  // This returns the XML header including the encoding:
  // The default is this: "<?version="1.0" encoding="utf-8"?>
  const std::string CreateXmlHeader() const;

  // These methods access the XML encoding of the XML file.
  void set_encoding(const std::string& encoding) {
    encoding_ = encoding;
  }
  const std::string& get_encoding() const {
    return encoding_;
  }

  // This returns the Object Element with the given id.  A NULL Object is
  // returned if no Object with this id exists in the KML file.
  kmldom::ObjectPtr GetObjectById(std::string id);

  // This returns the shared StyleSelector Element with the given id.  NULL is
  // returned if no StyleSelector with this id exists as a shared style
  // selector in the KML file.
  kmldom::StyleSelectorPtr GetSharedStyleById(std::string id);

  // TODO: set/get the default xmlns and prefix-namespace mappings
  // TODO: set/get URL of this KmlFile

 private:
  // These are helper functions for CreateFromParse().
  bool _CreateFromParse(const std::string& kml_or_kmz_data,
                        std::string* errors);
  bool OpenAndParseKmz(const std::string& kmz_data, std::string* errors);
  void Clear();
  std::string encoding_;
  std::string default_xmlns_;
  kmldom::ElementPtr root_;
  object_id_map_t object_id_map_;
  shared_style_map_t shared_style_map_;
  boost::scoped_ptr<kmlengine::KmzFile> kmz_file_;
  LIBKML_DISALLOW_EVIL_CONSTRUCTORS(KmlFile);
};

}  // end namespace kmlengine

#endif  // KML_ENGINE_KML_FILE_H__
