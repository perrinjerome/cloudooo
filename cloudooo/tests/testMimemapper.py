##############################################################################
#
# Copyright (c) 2002-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Gabriel M. Monnerat <gabriel@tiolive.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import unittest
from cloudoooTestCase import cloudoooTestCase
from cloudooo.application.openoffice import openoffice
from cloudooo.mimemapper import MimeMapper
from cloudoooTestCase import make_suite

text_expected_tuple = (('doc', 'Microsoft Word 6.0'),
    ('doc', 'Microsoft Word 95'),
    ('doc', 'Microsoft Word 97/2000/XP'), 
    ('htm', 'HTML Document (OpenOffice.org Writer)'),
    ('html', 'HTML Document (OpenOffice.org Writer)'), 
    ('html', 'XHTML'), ('odt', 'ODF Text Document'), 
    ('ott', 'ODF Text Document Template'), 
    ('pdf', 'PDF - Portable Document Format'), 
    ('rtf', 'Rich Text Format'), ('sdw', 'StarWriter 3.0'),
    ('sdw', 'StarWriter 4.0'), ('sdw', 'StarWriter 5.0'), 
    ('sxw', 'OpenOffice.org 1.0 Text Document'),
    ('txt', 'Text'), ('txt', 'Text Encoded'), 
    ('xhtml', 'XHTML'),
    (u'pdb', u'AportisDoc (Palm)'),
    (u'psw', u'Pocket Word'))

global_expected_tuple = (('sdw', 'StarWriter 3.0'),
    ('sdw', 'StarWriter 4.0'),
    ('sgl', 'StarWriter 4.0 Master Document'),
    ('sdw', 'StarWriter 5.0'),
    ('sgl', 'StarWriter 5.0 Master Document'),
    ('txt', 'Text Encoded (OpenOffice.org Master Document)'),
    ('sxw', 'OpenOffice.org 1.0 Text Document'),
    ('sxg', 'OpenOffice.org 1.0 Master Document'),
    ('pdf', 'PDF - Portable Document Format'),
    ('odm', 'ODF Master Document'),
    ('odt', 'ODF Text Document'),
    ('html', 'HTML (Writer/Global)'),
    ('htm', 'HTML (Writer/Global)'))

drawing_expected_tuple = (('bmp', 'BMP - Windows Bitmap'), 
    ('emf', 'EMF - Enhanced Metafile'), 
    ('eps', 'EPS - Encapsulated PostScript'),
    ('gif', 'GIF - Graphics Interchange Format'), 
    ('htm', 'HTML Document (OpenOffice.org Draw)'),
    ('html', 'HTML Document (OpenOffice.org Draw)'),
    ('html', 'XHTML'), 
    ('jfif', 'JPEG - Joint Photographic Experts Group'),
    ('jif', 'JPEG - Joint Photographic Experts Group'),
    ('jpe', 'JPEG - Joint Photographic Experts Group'), 
    ('jpeg', 'JPEG - Joint Photographic Experts Group'),
    ('jpg', 'JPEG - Joint Photographic Experts Group'), 
    ('met', 'MET - OS/2 Metafile'), ('odg', 'ODF Drawing'),
    ('otg', 'ODF Drawing Template'), ('pbm', 'PBM - Portable Bitmap'),
    ('pct', 'PCT - Mac Pict'),
    ('pdf', 'PDF - Portable Document Format'),
    ('pgm', 'PGM - Portable Graymap'),
    ('pict', 'PCT - Mac Pict'),
    ('png', 'PNG - Portable Network Graphic'),
    ('ppm', 'PPM - Portable Pixelmap'),
    ('ras', 'RAS - Sun Raster Image'), ('sda', 'StarDraw 5.0'),
    ('sdd', 'StarDraw 3.0'), 
    ('svg', 'SVG - Scalable Vector Graphics'),
    ('svm', 'SVM - StarView Metafile'),
    ('sxd', 'OpenOffice.org 1.0 Drawing'), 
    ('tif', 'TIFF - Tagged Image File Format'),
    ('tiff', 'TIFF - Tagged Image File Format'),
    ('wmf', 'WMF - Windows Metafile'),
    ('xhtml', 'XHTML'), ('xpm', 'XPM - X PixMap'))

web_expected_tuple = (('html', 'HTML Document'),
    ('htm', 'HTML Document'),
    ('txt', 'Text (OpenOffice.org Writer/Web)'), 
    ('txt', 'Text Encoded (OpenOffice.org Writer/Web)'),
    ('sxw', 'OpenOffice.org 1.0 Text Document (OpenOffice.org Writer/Web)'),
    ('pdf', 'PDF - Portable Document Format'),
    ('odt', 'OpenOffice.org Text (OpenOffice.org Writer/Web)'),
    ('sdw', 'StarWriter 3.0 (OpenOffice.org Writer/Web)'),
    ('sdw', 'StarWriter 4.0 (OpenOffice.org Writer/Web)'),
    ('sdw', 'StarWriter 5.0 (OpenOffice.org Writer/Web)'))

presentation_expected_tuple = (('bmp', 'BMP - Windows Bitmap'),
    ('emf', 'EMF - Enhanced Metafile'),
    ('eps', 'EPS - Encapsulated PostScript'),
    ('gif', 'GIF - Graphics Interchange Format'),
    ('htm', 'HTML Document (OpenOffice.org Impress)'),
    ('html', 'HTML Document (OpenOffice.org Impress)'),
    ('html', 'XHTML'), ('jfif', 'JPEG - Joint Photographic Experts Group'),
    ('jif', 'JPEG - Joint Photographic Experts Group'),
    ('jpe', 'JPEG - Joint Photographic Experts Group'),
    ('jpeg', 'JPEG - Joint Photographic Experts Group'),
    ('jpg', 'JPEG - Joint Photographic Experts Group'),
    ('met', 'MET - OS/2 Metafile'), ('odg', 'ODF Drawing (Impress)'),
    ('odp', 'ODF Presentation'), ('otp', 'ODF Presentation Template'),
    ('pbm', 'PBM - Portable Bitmap'), ('pct', 'PCT - Mac Pict'),
    ('pdf', 'PDF - Portable Document Format'),
    ('pgm', 'PGM - Portable Graymap'), 
    ('pict', 'PCT - Mac Pict'),
    ('png', 'PNG - Portable Network Graphic'),
    ('pot', 'Microsoft PowerPoint 97/2000/XP Template'),
    ('ppm', 'PPM - Portable Pixelmap'),
    ('pps', 'Microsoft PowerPoint 97/2000/XP'),
    ('ppt', 'Microsoft PowerPoint 97/2000/XP'),
    ('ras', 'RAS - Sun Raster Image'),
    ('sda', 'StarDraw 5.0 (OpenOffice.org Impress)'),
    ('sdd', 'StarDraw 3.0 (OpenOffice.org Impress)'),
    ('sdd', 'StarImpress 4.0'), ('sdd', 'StarImpress 5.0'),
    ('svg', 'SVG - Scalable Vector Graphics'),
    ('svm', 'SVM - StarView Metafile'),
    ('sxd', 'OpenOffice.org 1.0 Drawing (OpenOffice.org Impress)'),
    ('sxi', 'OpenOffice.org 1.0 Presentation'),
    ('tif', 'TIFF - Tagged Image File Format'), 
    ('tiff', 'TIFF - Tagged Image File Format'),
    ('wmf', 'WMF - Windows Metafile'),
    ('xhtml', 'XHTML'), ('xpm', 'XPM - X PixMap'))

spreadsheet_expected_tuple = (('csv', 'Text CSV'), 
    ('htm', 'HTML Document (OpenOffice.org Calc)'),
    ('html', 'HTML Document (OpenOffice.org Calc)'),
    ('html', 'XHTML'), ('ods', 'ODF Spreadsheet'),
    ('ots', 'ODF Spreadsheet Template'), 
    ('pdf', 'PDF - Portable Document Format'),
    ('sdc', 'StarCalc 3.0'), ('sdc', 'StarCalc 4.0'),
    ('sdc', 'StarCalc 5.0'), ('sxc', 'OpenOffice.org 1.0 Spreadsheet'),
    ('txt', 'Text CSV'), ('xhtml', 'XHTML'),
    ('xlc', 'Microsoft Excel 4.0'), ('xlc', 'Microsoft Excel 5.0'),
    ('xlc', 'Microsoft Excel 95'), ('xlc', 'Microsoft Excel 97/2000/XP'),
    ('xlm', 'Microsoft Excel 4.0'), ('xlm', 'Microsoft Excel 5.0'),
    ('xlm', 'Microsoft Excel 95'), ('xlm', 'Microsoft Excel 97/2000/XP'),
    ('xls', 'Microsoft Excel 4.0'), ('xls', 'Microsoft Excel 5.0'),
    ('xls', 'Microsoft Excel 95'), ('xls', 'Microsoft Excel 97/2000/XP'),
    ('xls', 'Text CSV'), ('xlt', 'Microsoft Excel 5.0 Template'),
    ('xlt', 'Microsoft Excel 95 Template'),
    ('xlt', 'Microsoft Excel 97/2000/XP Template'),
    ('xlw', 'Microsoft Excel 4.0'), ('xlw', 'Microsoft Excel 5.0'),
    ('xlw', 'Microsoft Excel 95'), ('xlw', 'Microsoft Excel 97/2000/XP'))

math_expected_tuple = (('smf', 'StarMath 4.0'), ('mml', 'MathML 1.01'),
    ('pdf', 'PDF - Portable Document Format'), ('smf', 'StarMath 5.0'),
    ('sxm', 'OpenOffice.org 1.0 Formula'), ('odf', 'ODF Formula'), 
    ('smf', 'StarMath 3.0'))

chart_expected_tuple = (('sds', 'StarChart 3.0'),
    ('sds', 'StarChart 4.0'),
    ('sds', 'StarChart 5.0'),
    ('sxs', 'OpenOffice.org 1.0 Chart'),
    ('odc', 'ODF Chart'))

class TestMimeMapper(cloudoooTestCase):
  """Test if object load filters correctly of OOo."""

  def afterSetUp(self):
    """Mimemapper is created and load uno path."""
    self.mimemapper = MimeMapper()
    openoffice.acquire()
    hostname, port = openoffice.getAddress()
    self.mimemapper.loadFilterList(hostname,
                                  port,
                                  unomimemapper_bin=self.unomimemapper_bin, 
                                  python_path=self.python_path)
    openoffice.release()

  def testUnoMimemapperPath(self):
    """Test if the unomimemapper has the path to script"""
    mimemapper = MimeMapper()
    openoffice.acquire()
    hostname, port = openoffice.getAddress()
    try:
      mimemapper.loadFilterList(hostname, port)
    except:
      self.assertEquals(mimemapper.unomimemapper_bin, "/usr/bin/unomimemapper.py")
    finally:
      openoffice.release()
    openoffice.acquire()
    try:
      mimemapper.loadFilterList(hostname, port, unomimemapper_bin="/x/y/unomimemapper")
    except NameError:
      self.assertEquals(mimemapper.unomimemapper_bin, "/x/y/unomimemapper")
    finally:
      openoffice.release()

  def testGetFilterWhenExtensionNotExist(self):
    """Test the case that the user passes extension which does not exist."""
    empty_list = self.mimemapper.getFilterList('xxx')
    self.assertEquals(empty_list, [])
 
  def testIfThereIsDuplicateData(self):
    """Test if there is duplicate data."""
    extension_list = self.mimemapper._doc_type_list_by_extension.keys()
    self.assertEquals(len(extension_list), len(set(extension_list)))
    for type_list in self.mimemapper._doc_type_list_by_extension.values():
      self.assertEquals(len(type_list), len(set(type_list)))
    document_type_list = self.mimemapper._document_type_dict.keys()
    self.assertEquals(len(document_type_list), len(set(document_type_list)))
    document_service_list = self.mimemapper._document_type_dict.values()
    self.assertEquals(len(document_service_list), len(set(document_service_list)))
    document_service_list = self.mimemapper._extension_list_by_type.keys()
    self.assertEquals(len(document_service_list), len(set(document_service_list)))
    extension_list = self.mimemapper._extension_list_by_type.values()
    for extension in extension_list:
      self.assertEquals(len(extension), len(set(extension)),
          "extension_list_by_type has duplicate data")

  def testGetFilterByExt(self):
    """Test if passing the extension the filter returns corretcly."""
    pdf_filter_list = self.mimemapper.getFilterList('pdf')
    self.assertEquals(len(pdf_filter_list),7)
    xls_filter_list = self.mimemapper.getFilterList('xls')
    self.assertEquals(len(xls_filter_list),5)
    doc_filter_list = self.mimemapper.getFilterList('doc')
    self.assertEquals(len(doc_filter_list),3)

  def testGetDocumentTypeDict(self):
    """Test if dictonary document type returns type correctly."""
    document_type_dict = self.mimemapper._document_type_dict
    type = document_type_dict.get("text")
    self.assertEquals(type, 'com.sun.star.text.TextDocument')
    type = document_type_dict.get("chart")
    self.assertEquals(type, 'com.sun.star.chart2.ChartDocument')
    type = document_type_dict.get("drawing")
    self.assertEquals(type, 'com.sun.star.drawing.DrawingDocument')
    type = document_type_dict.get("presentation")
    self.assertEquals(type, 'com.sun.star.presentation.PresentationDocument')
    type = document_type_dict.get("spreadsheet")
    self.assertEquals(type, 'com.sun.star.sheet.SpreadsheetDocument')
    type = document_type_dict.get("web")
    self.assertEquals(type, 'com.sun.star.text.WebDocument')

  def testGetAllowedExtensionListByExtension(self):
    """Test if function getAllowedExtensionList returns correctly a list with 
    extensions that can generate with extension passed."""
    doc_got_list = list(self.mimemapper.getAllowedExtensionList('doc'))
    doc_got_list.sort()
    text_expected_list = list(text_expected_tuple)
    text_expected_list.sort()
    self.assertEquals(doc_got_list, text_expected_list)
    jpeg_got_list = list(self.mimemapper.getAllowedExtensionList('jpeg'))
    jpeg_got_list.sort()
    jpeg_expected_list = list(set(presentation_expected_tuple + 
        drawing_expected_tuple))
    jpeg_expected_list.sort()
    self.assertEquals(jpeg_got_list, jpeg_expected_list)
    pdf_got_list = list(self.mimemapper.getAllowedExtensionList('pdf'))
    pdf_got_list.sort()
    pdf_expected_list = list(set(presentation_expected_tuple +
      drawing_expected_tuple + web_expected_tuple + global_expected_tuple + 
      math_expected_tuple + text_expected_tuple + spreadsheet_expected_tuple))
    pdf_expected_list.sort()
    self.assertEquals(pdf_got_list, pdf_expected_list)
  
  def testGetAllowedExtensionListForText(self):
    """Passing document_type equal to 'text', the return must be equal
    to text_expected_tuple."""
    got_list = list(self.mimemapper.getAllowedExtensionList(document_type='text'))
    got_list.sort()
    text_expected_list = list(text_expected_tuple)
    text_expected_list.sort()
    self.assertEquals(got_list, text_expected_list)

  def testGetAllowedExtensionListForGlobal(self):
    """Passing document_type equal to 'global', the return must be equal
    to global_expected_tuple."""
    got_list = list(self.mimemapper.getAllowedExtensionList(document_type='global'))
    got_list.sort()
    global_expected_list = list(global_expected_tuple)
    global_expected_list.sort()
    self.assertEquals(got_list, global_expected_list)

  def testGetAllAllowedExtensionListForDrawing(self):
    """Passing document_type equal to 'drawing', the return must be equal
    to drawing_expected_tuple."""
    got_list = list(self.mimemapper.getAllowedExtensionList(document_type='drawing'))
    got_list.sort()
    drawing_expected_list = list(drawing_expected_tuple)
    drawing_expected_list.sort()
    self.assertEquals(got_list, drawing_expected_list)

  def testGetAllAllowedExtensionListForWeb(self):
    """Passing document_type equal to 'web', the return must be equal
    to web_expected_tuple."""
    got_tuple = list(self.mimemapper.getAllowedExtensionList(document_type='web'))
    got_tuple.sort()
    web_expected_list = list(web_expected_tuple)
    web_expected_list.sort()
    self.assertEquals(got_tuple, web_expected_list)

  def testGetAllAllowedExtensionListForPresentation(self):
    """Passing document_type equal to 'presentation', the return must be equal
    to presentation_expected_tuple."""
    got_list = \
        list(self.mimemapper.getAllowedExtensionList(document_type='presentation'))
    got_list.sort()
    presentation_expected_list = list(presentation_expected_tuple)
    presentation_expected_list.sort()
    self.assertEquals(got_list, presentation_expected_list)

  def testGetAllAllowedExtensionListForSpreadsheet(self):
    """Passing document_type equal to 'spreadsheet', the return must be equal
    to spreadsheet_expected_tuple."""
    got_tuple = self.mimemapper.getAllowedExtensionList(document_type='spreadsheet')
    self.assertEquals(sorted(got_tuple), sorted(spreadsheet_expected_tuple))

  def testGetAllAllowedExtensionListForChart(self):
    """Passing document_type equal to 'chart', the return must be equal
    to chart_expected_tuple."""
    got_list = list(self.mimemapper.getAllowedExtensionList(document_type='chart'))
    got_list.sort()
    chart_expected_list = list(chart_expected_tuple)
    chart_expected_list.sort()
    self.assertEquals(got_list, chart_expected_list)

  def testGetFilterName(self):
    """Test if passing extension and document_type, the filter is correct."""
    filtername = self.mimemapper.getFilterName("pdf", 'com.sun.star.text.TextDocument')
    self.assertEquals(filtername, "writer_pdf_Export")
    filtername = self.mimemapper.getFilterName('ppt', 'com.sun.star.presentation.PresentationDocument')
    self.assertEquals(filtername,"MS PowerPoint 97")
    filtername = self.mimemapper.getFilterName("html", 'com.sun.star.presentation.PresentationDocument')
    self.assertEquals(filtername, "impress_html_Export")

  
  def testGetMimetype(self):
    """Test get mimetype according to the filter type"""
    self.assertEquals(self.mimemapper.getMimetypeByFilterType("writer8"),\
        "application/vnd.oasis.opendocument.text")
    self.assertEquals(self.mimemapper.getMimetypeByFilterType("math8"),\
        "application/vnd.oasis.opendocument.formula")
    self.assertEquals(self.mimemapper.getMimetypeByFilterType("writer_MS_Word_97"),\
        'application/msword')

def test_suite():
  return make_suite(TestMimeMapper)

if '__main__' == __name__:
  from cloudoooTestCase import startFakeEnvironment, stopFakeEnvironment
  startFakeEnvironment()
  suite = unittest.TestLoader().loadTestsFromTestCase(TestMimeMapper)
  unittest.TextTestRunner(verbosity=2).run(suite)
  stopFakeEnvironment()
