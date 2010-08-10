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

import jsonpickle
from os import environ
from subprocess import Popen, PIPE
from cloudooo.application.openoffice import openoffice
from zope.interface import implements
from cloudooo.interfaces.handler import IHandler
from cloudooo.mimemapper import mimemapper
from cloudooo.document import FileSystemDocument
from cloudooo.monitor.timeout import MonitorTimeout
from cloudooo.utils import logger
from psutil import pid_exists

class OOHandler:
  """OOHandler is used to access the one Document and OpenOffice.
  
  For each Document inputed is created on instance of this class to manipulate
  the document. This Document must be able to create and remove a temporary
  document at FS, load, export and export.
  """
  implements(IHandler)

  def __init__(self, base_folder_url, data, source_format, **kw):
    """Creates document in file system and loads it in OOo."""
    self.document = FileSystemDocument(base_folder_url,
                                      data,
                                      source_format)
    self.zip = kw.get('zip', False)
    self.uno_path = kw.get("uno_path", None)
    self.office_bin_path = kw.get("office_bin_path", None)
    self.timeout = kw.get("timeout", 600)
    self.unoconverter_bin = kw.get('unoconverter_bin', "unoconverter")
    self.source_format = source_format
    self.python_path = kw.get('python_path', 'python')
    if not self.uno_path:
      self.uno_path = environ.get("uno_path")
    if not self.office_bin_path:
      self.office_bin_path = environ.get("office_bin_path")

  def _getCommand(self, *args, **kw):
    """Transforms all parameters passed in a command"""
    hostname, port = openoffice.getAddress()
    kw['hostname'] = hostname
    kw['port'] = port
    command_list = [self.python_path
        , self.unoconverter_bin
        , "--uno_path='%s'" % self.uno_path
        , "--office_bin_path='%s'" % self.office_bin_path
        , "--document_url='%s'" % self.document.getUrl()]
    for arg in args:
      command_list.insert(2, "--%s" % arg)
    for k, v in kw.iteritems():
      command_list.append("--%s='%s'" % (k,v))
      
    return ' '.join(command_list)
  
  def _startTimeout(self):
    """start the Monitor"""
    self.monitor = MonitorTimeout(openoffice, self.timeout)
    self.monitor.start()
    return

  def _stopTimeout(self):
    """stop the Monitor"""
    self.monitor.terminate()
    return

  def _subprocess(self, command):
    """Run one procedure"""
    try:
      self._startTimeout()
      process = Popen(command,
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE,
                    close_fds=True)
      stdout, stderr = process.communicate()
    finally:
      self._stopTimeout()
      if pid_exists(process.pid):
        process.terminate()
    return stdout, stderr

  def _callUnoConverter(self, *feature_list, **kw):
    """ """
    if not openoffice.status():
      openoffice.start()
    command = self._getCommand(*feature_list, **kw)
    stdout, stderr = self._subprocess(command)
    if not stdout and stderr != '':
      logger.debug(stderr)
      if "NoConnectException" in stderr or \
         "RuntimeException" in stderr or \
         "DisposedException" in stderr:
        self.document.restoreOriginal()
        openoffice.restart()
        kw['document_url'] = self.document.getUrl()
        command = self._getCommand(*feature_list, **kw)
        stdout, stderr = self._subprocess(command)
      elif "ErrorCodeIOException" in stderr:
        raise Exception, stderr + \
            "This document can not be converted to this format"
      else:
        raise Exception, stderr

    return stdout, stderr

  def convert(self, destination_format=None, **kw):
    """Convert a document to another format supported by the OpenOffice
    
    Keyword Arguments:
    destination_format -- extension of document as String
    """
    logger.debug("Convert: %s > %s" % (self.source_format, destination_format))
    openoffice.acquire()
    kw['source_format'] = self.source_format
    if destination_format:
      kw['destination_format'] = destination_format
      kw['mimemapper'] = jsonpickle.encode(mimemapper)
    try:
      stdout, stderr = self._callUnoConverter(*['convert'], **kw)
    finally:
      openoffice.release()
      if self.monitor.is_alive():
        self._stopTimeout()
    url = stdout.replace('\n', '')
    self.document.reload(url)
    content = self.document.getContent(self.zip)
    self.document.trash()
    return content

  def getMetadata(self, base_document=False):
    """Returns a dictionary with all metadata of document.
    
    Keywords Arguments:
    base_document -- Boolean variable. if true, the document is also returned
    along with the metadata."""
    openoffice.acquire()
    mimemapper_pickled = jsonpickle.encode(mimemapper)
    logger.debug("getMetadata")
    kw = dict(mimemapper=mimemapper_pickled)
    if base_document:
      feature_list = ['getmetadata', 'convert']
    else:
      feature_list = ['getmetadata']
    try:
      stdout, stderr = self._callUnoConverter(*feature_list, **kw)
    finally:
      openoffice.release()
      if self.monitor.is_alive():
        self._stopTimeout()
    metadata={}
    exec("metadata=%s" % stdout)
    if metadata.get("Data"):
      self.document.reload(metadata['Data'])
      metadata['Data'] = self.document.getContent()
    else:
      metadata['Data'] = ''
    self.document.trash() 
    return metadata
   
  def setMetadata(self, metadata):
    """Returns a document with new metadata.
    
    Keyword arguments:
    metadata -- expected an dictionary with metadata.
    """
    openoffice.acquire()
    metadata_pickled = jsonpickle.encode(metadata)
    logger.debug("setMetadata")
    kw = dict(metadata=metadata_pickled)
    try:
      stdout, stderr = self._callUnoConverter(*['setmetadata'], **kw)
    finally:
      openoffice.release()
      if self.monitor.is_alive():
        self._stopTimeout()
    doc_loaded = self.document.getContent()
    self.document.trash()
    return doc_loaded