import unittest
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX

class KmlFactoryTestCase(unittest.TestCase):
    
    def test_get_factory_object_name(self):
        "Tests obtaining a factory object"
        from pykml.factory import get_factory_object_name
        
        self.assertEqual(
            get_factory_object_name('http://www.opengis.net/kml/2.2'),
            'KML'
        )
        self.assertEqual(
            get_factory_object_name('http://www.w3.org/2005/Atom'),
            'ATOM'
        )
        self.assertEqual(get_factory_object_name(None), 'KML')
    
    def test_trivial_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        doc = KML.kml()
        schema = Schema("ogckml22.xsd")
        self.assertTrue(schema.validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2"/>'
        )
    
    def test_basic_kml_document(self):
        """Tests the creation of a basic OGC KML document."""
        doc = KML.kml(
            KML.Document(
                KML.name("KmlFile"),
                KML.Placemark(
                    KML.name("Untitled Placemark"),
                    KML.Point(
                        KML.coordinates("-95.265,38.959,0")
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<name>KmlFile</name>'
                '<Placemark>'
                  '<name>Untitled Placemark</name>'
                  '<Point>'
                    '<coordinates>-95.265,38.959,0</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )
    
    def test_basic_kml_document(self):
        """Tests the creation of a basic KML with Google Extensions ."""
        doc = KML.kml(
            GX.Tour(
                GX.Playlist(
                    GX.SoundCue(
                        KML.href("http://dev.keyhole.com/codesite/cntowerfacts.mp3")
                    ),
                    GX.Wait(
                        GX.duration(10)
                    ),
                    GX.FlyTo(
                        GX.duration(5),
                        GX.flyToMode("bounce"),
                        KML.LookAt(
                            KML.longitude(-79.387),
                            KML.latitude(43.643),
                            KML.altitude(0),
                            KML.heading(-172.3),
                            KML.tilt(10),
                            KML.range(1200),
                            KML.altitudeMode("relativeToGround"),
                        )
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<gx:Tour>'
                '<gx:Playlist>'
                  '<gx:SoundCue>'
                    '<href>http://dev.keyhole.com/codesite/cntowerfacts.mp3</href>'
                  '</gx:SoundCue>'
                  '<gx:Wait>'
                    '<gx:duration>10</gx:duration>'
                  '</gx:Wait>'
                  '<gx:FlyTo>'
                    '<gx:duration>5</gx:duration>'
                    '<gx:flyToMode>bounce</gx:flyToMode>'
                    '<LookAt>'
                      '<longitude>-79.387</longitude>'
                      '<latitude>43.643</latitude>'
                      '<altitude>0</altitude>'
                      '<heading>-172.3</heading>'
                      '<tilt>10</tilt>'
                      '<range>1200</range>'
                      '<altitudeMode>relativeToGround</altitudeMode>'
                    '</LookAt>'
                  '</gx:FlyTo>'
                '</gx:Playlist>'
              '</gx:Tour>'
            '</kml>'
        )
    
    def test_kml_document_with_atom_element(self):
        """Tests the creation of a KML document with an ATOM element."""
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. KML. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        self.assertTrue(Schema("kml22gx.xsd").validate(doc))
        self.assertEquals(
            etree.tostring(doc),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<atom:author>'
                  '<atom:name>J. KML. Rowling</atom:name>'
                '</atom:author>'
                '<atom:link href="http://www.harrypotter.com"/>'
                '<Placemark>'
                  '<name>Hogwarts</name>'
                  '<Point>'
                    '<coordinates>1,1</coordinates>'
                  '</Point>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )


class GeneratePythonScriptTestCase(unittest.TestCase):
    
    def test_write_python_script_for_kml_document(self):
        """Tests the creation of a trivial OGC KML document."""
        from pykml.factory import write_python_script_for_kml_document
        
        doc = KML.kml(
            KML.Document(
                ATOM.author(
                    ATOM.name("J. K. Rowling")
                ),
                ATOM.link(href="http://www.harrypotter.com"),
                KML.Placemark(
                    KML.name("Hogwarts"),
                    KML.Point(
                        KML.coordinates("1,1")
                    )
                )
            )
        )
        script = write_python_script_for_kml_document(doc)
        self.assertEquals(
            script,
            'from pykml.factory import KML_ElementMaker as KML\n'
            'from pykml.factory import ATOM_ElementMaker as ATOM\n'
            'from pykml.factory import GX_ElementMaker as GX\n'
            '\n'
            'doc = KML.kml(\n'
            '  KML.Document(\n'
            '    ATOM.author(\n'
            '      ATOM.name("J. K. Rowling"),\n'
            '    ),\n'
            '    ATOM.link(href="http://www.harrypotter.com",),\n'
            '    KML.Placemark(\n'
            '      KML.name("Hogwarts"),\n'
            '      KML.Point(\n'
            '        KML.coordinates("1,1"),\n'
            '      ),\n'
            '    ),\n'
            '  ),\n'
            ')\n'
            'from lxml import etree\n'
            'print etree.tostring(doc,pretty_print=True)\n'
        )

#    def test_write_python_script_for_kml_document_with_cdata(self):
#        """Tests the creation of an OGC KML document with a cdata tag"""
#        
#        from pykml.factory import write_python_script_for_kml_document
#        
#        doc = KML.kml(
#            KML.Document(
#                KML.Placemark(
#                    KML.name("CDATA example"),
#                    KML.description(
#                        '<h1>CDATA Tags are useful!</h1>'
#                        '<p><font color="red">Text is <i>more readable</i> and '
#                        '<b>easier to write</b> when you can avoid using entity '
#                        'references.</font></p>'
#                    ),
#                ),
#                KML.Point(
#                    KML.coordinates("102.595626,14.996729"),
#                )
#            )
#        )
#        script = write_python_script_for_kml_document(doc)
#        self.assertEquals(script,
#"""from pykml.factory import KML_ElementMaker as KML
#from pykml.factory import ATOM_ElementMaker as ATOM
#from pykml.factory import GX_ElementMaker as GX
#
#doc = KML.kml(
#  KML.Document(
#    KML.Placemark(
#      KML.name("CDATA example"),
#      KML.description("<h1>CDATA Tags are useful!</h1><p><font color="red">Text is <i>more readable</i> and <b>easier to write</b> when you can avoid using entity references.</font></p>"),
#    ),
#    KML.Point(
#      KML.coordinates("102.595626,14.996729"),
#    ),
#  ),
#)
#from lxml import etree
#print etree.tostring(doc,pretty_print=True)
#"""
#)


    def test_write_python_script_for_kml_document_with_cdata2(self):
        """Tests the creation of an OGC KML document with a cdata tag"""
        
        from pykml.factory import write_python_script_for_kml_document
        
        doc = KML.kml(
            KML.Document(
                KML.Placemark(
                    KML.name("CDATA example"),
                    KML.description(
                        '<h1>CDATA Tags are useful!</h1>'
                        '<p><font color="red">Text is <i>more readable</i> and '
                        '<b>easier to write</b> when you can avoid using entity '
                        'references.</font></p>'
                    ),
                ),
                KML.Point(
                    KML.coordinates("102.595626,14.996729"),
                )
            )
        )
        script = write_python_script_for_kml_document(doc)
        self.assertEquals(
            script,
            'from pykml.factory import KML_ElementMaker as KML\n'
            'from pykml.factory import ATOM_ElementMaker as ATOM\n'
            'from pykml.factory import GX_ElementMaker as GX\n'
            '\n'
            'doc = KML.kml(\n'
            '  KML.Document(\n'
            '    KML.Placemark(\n'
            '      KML.name("CDATA example"),\n'
            '      KML.description("<![CDATA['
                     '<h1>CDATA Tags are useful!</h1>'
                     '<p><font color="red">Text is <i>more readable</i> and '
                     '<b>easier to write</b> when you can avoid using entity '
                     'references.</font></p>'
                     ']]>"),\n'
            '    ),\n'
            '    KML.Point(\n'
            '      KML.coordinates("102.595626,14.996729"),\n'
            '    ),\n'
            '  ),\n'
            ')\n'
            'from lxml import etree\n'
            'print etree.tostring(doc,pretty_print=True)\n'
        )
        print script


if __name__ == '__main__':
    unittest.main()