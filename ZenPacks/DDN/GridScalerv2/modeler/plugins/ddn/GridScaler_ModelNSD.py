# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 10:12:01 2015

@author: naveen
"""
__author__ = "Naveen Subramani"

import logging

log = logging.getLogger('zen.zenpymodelCluster')

from ZenPacks.DDN.GridScalerv2.lib import DDNRunCmd as gsc
from ZenPacks.DDN.GridScalerv2.lib import DDNGsUtil as gs
from ZenPacks.DDN.GridScalerv2.lib.DDNModelPlugin import DDNModelPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

# import pdb

class GridScaler_ModelNSD(DDNModelPlugin):
    """ Models GridScaler NSD Nodes """
    relname = "nsdNodes"
    modname = 'ZenPacks.DDN.GridScalerv2.NsdNode'

    def prepTask(self, device, log):
        log.debug("Module : NSD, Message : Preparing nsd info for %s",
                  device.id)
        cmdinfo = [{
                       'cmd':
                           '/opt/ddn/directmon/gridscaler/scripts/get_cluster_config.py',
                       'parser': gs.GsNSDCollector,
                       'filter': 'basic'},
                   {
                       'cmd':
                           '/opt/ddn/directmon/gridscaler/scripts/get_nodes_state.py',
                       'parser': gs.gsNSDStats,
                       'filter': 'state',
                   }]

        myCmds = []
        for c in cmdinfo:
            myCmds.append(gsc.Cmd(command=c['cmd'], template=c['filter'],
                                  config=self.config, parser=c['parser']))
        self.cmd = myCmds
        log.debug('Module : NSD, Message : XXX _prepNSDLists(): self.cmd = %r',
                  self.cmd)

    def parseResults(self, resultList):
        errmsgs = {}
        log.debug("Module : NSD, Message : XXX NSD _parseResults with " \
                  "resultList : %r ", resultList)
        rm = self.relMap()
        res = []  # aggregate list of dev/components maps
        omaps = []
        nsdServers = []
        for success, result in resultList:
            log.debug("Module : NSD, Message : XXX NSD __Result STATUS: %s" \
                      " and DATA: %s ", success, result)
            if success:
                if result.template == 'basic':
                    infoData = result.result
                    for key, val in infoData.items():
                        val = gs.dictflatten(val)
                        log.debug("Module : NSD, Message : XXX KEY: %s and" \
                                  " VALUE: %r", key, val)
                        # Update dict with id and title params
                        if val.get('id') is None:
                            val['id'] = str(key)
                        if val.get('title') is None:
                            val['title'] = str(key)
                        # Create Object Map
                        val['id'] = str('nsd_' + val.get('id'))
                        om = self.objectMap()
                        om.updateFromDict(val)
                        # Update Object Map to RelationShip Map
                        omaps.append(om)
                        nsdServers.append(str(key))

                elif result.template == 'state':
                    infoData = result.result
                    log.debug("Module : NSD, Message : XXXX nsd state: "
                              "result" \
                              " %r, type %s", infoData, type(infoData))
                    for key, val in infoData.items():
                        # val = gs.dictflatten(val)
                        log.debug("Module : NSD, Message : XXX KEY: %s and" \
                                  " VALUE: %r", key, val)
                        # Update dict with id and title params
                        for om in omaps:
                            log.debug("om.id %s", om.id)
                            if om.id == str('nsd_' + key):
                                setattr(om, 'state', str(val))
                                break
                else:
                    log.warn("Module : NSD, Message : XXX __Result is Not" \
                             " instance of Dict TYPE: %s RESULT: %r",
                             type(result.result),
                             result.result)
            else:
                errmsgs.update(str(result))

        for om in omaps: rm.append(om)
        devmod = {
                 # 'id': self.config.id,
                 # should not update id while updating attributes
                  # Update Current target as preferredNSD
                  'preferredNSD': self._conn_params['target'],
                  'nsdServers': nsdServers}
        devom = (ObjectMap(data=devmod,
                           modname='ZenPacks.DDN.GridScalerv2.GridScalerV2Device'))
        res.append(devom)
        log.debug("Module : NSD, collected NSDServers property: %r" % res)

        res.append(rm)
        d, self._task_defer = self._task_defer, None
        if d is None or d.called:
            return  # already processed, nothing to do now

        if errmsgs:
            log.error("Module : NSD, Message : XXX GridScalar SFA collection" \
                      " failed %s", str(errmsgs))
            d.callback([{}])
            return

        log.debug("XXX Collected GridScalar SAF DATA: %r", res)
        d.callback(res)

    def process(self, device, results, log):
        """ Process results, return iterable of data maps or None."""
        log.debug("Module : NSD, Message : XXX modeler process(dev=%r)" \
                  " got results %s ", device, str(results))
        return results


