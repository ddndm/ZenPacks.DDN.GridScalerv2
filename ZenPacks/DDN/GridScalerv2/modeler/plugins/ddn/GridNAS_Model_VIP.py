import logging

log = logging.getLogger('zen.zenpymodelClients')

from ZenPacks.DDN.GridScalerv2.lib import DDNRunCmd as gsc
from ZenPacks.DDN.GridScalerv2.lib import DDNGsUtil as gs
from ZenPacks.DDN.GridScalerv2.lib.DDNModelPlugin import DDNModelPlugin


class GridNAS_Model_VIP(DDNModelPlugin):
    """ Models GridNas Virtual Networks """
    relname = 'virtualNetworks'
    modname = 'ZenPacks.DDN.GridScalerv2.VirtualNetwork'

    def prepTask(self, device, log):
        self.device = device
        log.debug("%s: preparing for virtual ips", device.id)
        cmdinfo = [{
                       'cmd': 'nasctl vip_show',
                       'parser': gs.GridNasVipParse,
                       'filter': '',
                   }]

        myCmds = []
        for c in cmdinfo:
            myCmds.append(gsc.Cmd(command=c['cmd'], template=c['filter'],
                                  config=self.config, parser=c['parser']))
        self.cmd = myCmds
        log.debug('XXX _prepVipLists(): self.cmd = %r', self.cmd)

    def parseResults(self, resultList):
        errmsgs = {}  # any accumulated errors
        log.debug('XXXX within _parseResults with %r', resultList)
        rm = self.relMap()
        for success, result in resultList:
            log.debug("XXXX _parseResults (success/ds %s) %s", success, result)
            if success:
                if isinstance(result.result, dict):
                    info = result.result
                    for k, v in info.items():
                        v = gs.dictflatten(v)
                        log.debug('XXX vip %s, attribs %r', k, v)
                        # update dictionary for key properties
                        v['title'] = 'VirtualIP_{0}'.format(k)
                        om = self.objectMap()
                        om.updateFromDict(v)
                        rm.append(om)
                else:
                    log.warn('XXXX success result type %s value %r',
                             type(result.result), result.result)
            else:
                errmsgs.update(str(result))

        res = [rm]
        d, self._task_defer = self._task_defer, None
        if d is None or d.called:
            return  # already processed, nothing to do now

        if errmsgs:
            log.warn('XXXX GridNas VirtualIP collection failed %s',
                     str(errmsgs))
            ## TODO raise an event with data
            ## If error TODO pass an failed event
            d.callback([{}])
            return

        log.debug("collected GridNas VirtualIP property: %r" % res)
        d.callback(res)

    def process(self, device, results, log):
        """ Process results, return iterable of datamaps or None."""
        log.debug('XXXX modeler process(dev=%r) got results %s',
                  device, str(results))
        return results
