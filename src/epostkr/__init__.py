# -*- coding: utf-8 -*-
#
# epostkr: a client for epost.kr OpenAPI
# Copyright (C) 2012  mete0r (https://github.com/mete0r/)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class OpenAPI(object):
    ''' epost.go.kr OpenAPI '''

    def __init__(self, regkey):
        self.regkey = regkey

    #: OpenAPI 기본 요청 주소
    endpoint = 'http://biz.epost.go.kr/KpostPortal/openapi'

    def post_params(self, addr):
        ''' 우편번호 API 요청 변수

        :param addr: 주소 (unicode)
        :rtype: dict
        '''
        return dict(regkey=self.regkey,
                    target='post',
                    query=addr.encode('euc-kr'))

    def post_request(self, addr):
        ''' 우편번호 API 요청

        :param addr: 주소 (unicode)
        :return: urllib2.urlopen() 결과
        '''
        params = self.post_params(addr)
        import urllib, urllib2
        query = urllib.urlencode(params)
        return urllib2.urlopen(self.endpoint, query)

    def find_zipcodes_for(self, addr):
        ''' 주어진 주소로 우편번호를 검색한다.

        :param addr: 주소 (unicode)
        :return: 해당 주소로 검색된 우편번호와 상세 주소
        :rtype: generator of (우편번호, 상세주소)
        '''
        res = self.post_request(addr)

        # TODO: dirty hack: euc-kr seems not supported by ET
        body = res.read()
        # replace encoding in XMLDeclaration
        body = body.replace('euc-kr', 'utf-8')
        body = body.decode('euc-kr').encode('utf-8')

        from xml.etree import ElementTree as ET
        doc = ET.fromstring(body)
        itemlist = doc[0]
        for item in itemlist:
            address = item[0].text
            postcd = item[1].text
            yield postcd, address

def find_zipcodes():
    ''' 주어진 주소로 우편번호를 검색한다.
    '''
    from optparse import OptionParser
    import os.path

    usage = 'usage: %prog [options] <address>'
    parser = OptionParser(usage=usage)
    parser.add_option('-k', '--regkey', dest='regkey',
                      help='epost.go.kr OpenAPI regkey')
    parser.add_option('-f', '--regkey-file', dest='regkey_file',
                      default=os.path.expanduser('~/.epostkr.openapi.regkey'),
                      help='epost.go.kr OpenAPI regkey file [default: %default]')

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.error('<address> is required')
    else:
        import sys
        addr = args[0].decode(sys.getfilesystemencoding())

    if options.regkey:
        regkey = options.regkey.strip()
    elif options.regkey_file and os.path.exists(options.regkey_file):
        f = file(options.regkey_file, 'r')
        try:
            regkey = f.read().strip()
        finally:
            f.close()
    else:
        parser.error('-k or -f should be specified')

    api = OpenAPI(regkey)
    for zipcode, address in api.find_zipcodes_for(addr):
        print zipcode, address
