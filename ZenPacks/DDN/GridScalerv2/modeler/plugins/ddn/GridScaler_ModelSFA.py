# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:12:01 2015

@author: naveen
"""
__author__ = "Naveen Subramani"

import logging

log = logging.getLogger('zen.zenpymodelCluster')

from ZenPacks.DDN.GridScalerv2.lib import DDNRunCmd as gsc
from ZenPacks.DDN.GridScalerv2.lib import DDNGsUtil as gs
from ZenPacks.DDN.GridScalerv2.lib.DDNModelPlugin import DDNModelPlugin

# import pdb

class GridScaler_ModelSFA(DDNModelPlugin):
    """ Models GridScaler SFA """
    relname = "sfaNodes"
    modname = 'ZenPacks.DDN.GridScalerv2.SfaNode'

    def prepTask(self, device, log):
        log.debug("%s: preparing for SFA info", device.id)
        cmdinfo = [{
                       'cmd':
                           '/opt/ddn/directmon/gridscaler/scripts/get_cluster_config.py',
                       'parser': gs.GsSFAModelParser,
                       'filter': '',
                   }]

        myCmds = []
        for c in cmdinfo:
            myCmds.append(gsc.Cmd(command=c['cmd'], template=c['filter'],
                                  config=self.config, parser=c['parser']))
        self.cmd = myCmds
        log.debug('XXX _prepSFALists(): self.cmd = %r', self.cmd)

    def parseResults(self, resultList):
        errmsgs = {}
        log.debug("XXX _parseResults with resultList : %r ", resultList)
        rm = self.relMap()
        for success, result in resultList:
            log.debug("XXX __Result STATUS: %s and DATA: %s ", success, result)
            if success:
                if isinstance(result.result, dict):
                    infoData = result.result
                    for key, val in infoData.items():
                        val = gs.dictflatten(val)
                        log.debug("XXX KEY: %s and VALUE: %r", key, val)
                        # Update dict with id and title params
                        if val.get('id') is None:
                            val['id'] = str(key)
                        if val.get('title') is None:
                            val['title'] = str(key)
                        if val.get('device'):
                            val.pop('device')
                        if val.get('name'):
                            val.pop('name')

                        val['id'] = str('sfa_' + val.get('id'))
                        # Create Object Map
                        om = self.objectMap({'title': val['title'],
                                             'id': val['id'],
                                             'status': val['status']})
                        om.updateFromDict(val)
                        # Update Object Map to RelationShip Map
                        rm.append(om)
                else:
                    log.warn("XXX __Result is Not instance of Dict TYPE: %s "
                             "RESULT: %r", type(result.result), result.result)
            else:
                errmsgs.update(str(result))

        res = [rm]
        d, self._task_defer = self._task_defer, None
        if d is None or d.called:
            return  # already processed, nothing to do now

        if errmsgs:
            log.warn('XXX GridScalar SFA collection failed %s', str(errmsgs))
            d.callback([{}])
            return

        log.debug("XXX Collected GridScalar SAF DATA: %r", res)
        d.callback(res)

    def process(self, device, results, log):
        """ Process results, return iterable of data maps or None."""
        log.debug("XXX modeler process(dev=%r) got results %s ",
                  device, str(results))
        return results


