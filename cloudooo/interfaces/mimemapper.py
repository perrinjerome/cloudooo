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

from zope.interface import Interface

class IMimemapper(Interface):
  """Provide methods to manipulate filters of OOo."""

  def isLoaded():
    """Returns if the filters were loaded."""
    
  def getDocumentTypeDict():
    """Returns document type dict."""

  def getFilterName(extension, document_type):
    """Returns the name of filter according to parematers passed."""

  def loadFilterList(**kwargs):
    """Load all filters of openoffice."""

  def getFilterList(extension, **kwargs):
    """Returns a filter list according to extension or other parameters passed.
    """

  def getAllowedExtensionList(document_type, **kwargs):
    """Returns a list with extensions which can be used to export according to
    document type passed."""

  def getMimetypeByFilterType(filter_type):
    """Returns mimetype according to the filter type passed"""