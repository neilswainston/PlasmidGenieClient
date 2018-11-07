'''
PlasmidGenieClient (c) University of Manchester. 2018

PathwayGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
import json
import os
import sys

from synbiochem.utils import net_utils


class PlasmidGenieClient(object):
    '''PlasmidGenieClient class.'''

    def __init__(self, url='https://parts.synbiochem.co.uk'):
        self.__url = url if url[-1] == '/' else url + '/'

    def run(self, ice_params, filename, restr_enzs, melt_temp=70.0,
            circular=True):
        '''Run client.'''
        query = _get_query(ice_params, filename,
                           restr_enzs, melt_temp, circular)

        headers = {'Accept': 'application/json, text/plain, */*',
                   'Accept-Language': 'en-gb',
                   'Content-Type': 'application/json;charset=UTF-8'}

        resp = json.loads(net_utils.post(self.__url + 'submit',
                                         json.dumps(query),
                                         headers))

        print resp['job_ids'][0]


def _get_query(ice_params, filename, restr_enzs, melt_temp, circular):
    '''Return query.'''
    query = {u'designs': _get_designs(filename),
             u'app': 'PlasmidGenie',
             u'ice': ice_params,
             u'design_id': _get_design_id(filename),
             u'restr_enzs': restr_enzs,
             u'melt_temp': melt_temp,
             u'circular': circular}

    return query


def _get_design_id(filename):
    '''Get design id.'''
    _, tail = os.path.split(filename)
    return os.path.splitext(tail)[0]


def _get_designs(filename):
    '''Get designs.'''
    designs = []

    with open(filename) as fle:
        for line in fle:
            tokens = line.split()
            designs.append({'name': tokens[0], 'design': tokens[1:]})

    return designs


def main(args):
    '''main method.'''
    ice_params = {u'url': args[0],
                  u'username': args[1],
                  u'password': args[2],
                  u'groups': args[3]}

    client = PlasmidGenieClient()
    client.run(ice_params, filename=args[4], restr_enzs=args[5:])


if __name__ == '__main__':
    main(sys.argv[1:])
