##############################################################################
#
# Copyright (c) 2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Priscila Manhaes  <psilva@iff.edu.br>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
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

from os.path import join
from cloudooo.tests.cloudoooTestCase import TestCase, make_suite


class TestAllSupportedFormat(TestCase):

  def ConversionScenarioList(self):
    return [# XXX This might expect audio/octet-stream but only got audio/mpeg
            (join('data', 'test.ogg'), "ogg", "mp3", "audio/mpeg"),
            (join('data', 'test.ogg'), "ogg", "wav", "audio/x-wav"),
            (join('data', 'test.ogg'), "ogg", "midi", "audio/rtp-midi"),
            ]

  def testAllSupportedFormat(self):
    self.runConversionList(self.ConversionScenarioList())


def test_suite():
  return make_suite(TestAllSupportedFormat)
