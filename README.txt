epostkr: a client for epost.kr OpenAPI
======================================

see `epost.kr OpenAPI <http://biz.epost.go.kr/eportal/custom/custom_9.jsp?subGubun=sub_3&subGubun_1=cum_17&gubun=m07>`_.

Usage example::

    import epostkr
    openapi = epostkr.OpenAPI('my-api-key')
    for zipcode, address in openapi.find_zipcodes_for( u'구의1동' ):
        print zipcode, address
    
:License: `Affero GPL v3 <https://www.gnu.org/licenses/agpl-3.0.html>`_
:Author: mete0r
