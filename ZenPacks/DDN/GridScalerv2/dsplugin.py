# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 12:35:28 2015

@author: naveen
"""

__author__ = "Naveen Subramani"

# Logging
import logging

log = logging.getLogger('zen.zenpymetrics')

# DNN Lib files
from ZenPacks.DDN.GridScalerv2.lib import DDNRunCmd as gsc
from ZenPacks.DDN.GridScalerv2.lib import DDNGsUtil as gsu
from ZenPacks.DDN.GridScalerv2.lib.DDNMetricPlugin import DDNMetricPlugin

# PythonCollector Imports

from Products.ZenEvents import ZenEventClasses
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


GSMODEL = {None:
               {'modname': 'ZenPacks.DDN.GridScalerv2.GridScalerV2Device',
                'compname': '',
                'relname': ''},
           'fsLists':
               {'modname': 'ZenPacks.DDN.GridScalerv2.FsList',
                'compname': 'fsLists',
                'relname': 'fsLists'},
           'nsdNodes':
               {'modname': 'ZenPacks.DDN.GridScalerv2.NsdNode',
                'compname': 'nsdNodes',
                'relname': 'nsdNodes'},
           'sfaNodes':
               {'modname': 'ZenPacks.DDN.GridScalerv2.SfaNode',
                'compname': 'sfaNodes',
                'relname': 'sfaNodes'},
           'clientNodes':
               {'modname': 'ZenPacks.DDN.GridScalerv2.ClientNode',
                'compname': 'clientNodes',
                'relname': 'clientNodes'}
}

DEVMODEL = GSMODEL[None]


class GsFSMetricPlugin(DDNMetricPlugin):
    """ This plugin collects metrics for all gridscaler fs components """

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        log.debug("XXX GsMetricPlugin params(cls=%r, datasource=%r, context=%r"
                  % (cls, datasource, context))
        return {}

    def __init__(self):
        super(GsFSMetricPlugin, self).__init__()

    def parseMetricResults(self, results, notused):
        """ parse the results for each datasource part of config """
        log.debug("XXX parseMetricResults called (config:%s, results: %s)",
                  self.config, results)
        res = None
        for ds in self.config.datasources:
            # the below template is available as part of ds.points.id
            component = ds.component
            log.debug("DEVICE COMPONENT:    %s", component)

            if ds.template == 'GS_FsList':  # FS
                res = gsu.GsFsMetricsParser(results)
            else:
                # unexpected, log an error and return none
                log.error('XXXX unexpected datasource %r', ds)
                continue

        log.debug('XXX result=%s', (str(res)))
        return res

    def prepTask(self, config):
        cmds = ('/opt/ddn/directmon/gridscaler/scripts/get_mmdf_data.py',)
        for c in cmds:
            self.cmd.append(gsc.Cmd(command=c, template='metrics',
                                    config=self.config,
                                    parser=self.parseMetricResults))
        log.debug('XXX _prepMetricsCmd(): self.cmd = %r', self.cmd)

    def onSuccess(self, result, config):
        log.debug('XXXX FS Metric onSuccess: values is %s', str(result))
        aggregate = self.new_data()
        aggregate['values'] = result
        return aggregate

    def onError(self, result, config):
        log.error("XXXX onError(self=%r, result=%r, config=%r)",
                  self, result.getErrorMessage(), config)
        aggregate = self.new_data()
        aggregate['events'] = [{
                                   'component': '',
                                   'device': config.id,
                                   'summary': 'error connection failed %s' %
                                              str(self.conn_params),
                                   'eventClass': '/Perf',
                                   'eventKey': '/Perf/GridScalerV2/FSLIST',
                                   'severity': ZenEventClasses.Error,
                               }]
        return aggregate


class GsSfaMetricPlugin(DDNMetricPlugin):
    """This Class will collect metrics for SFA component"""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        log.debug("XXXX GsMetricPlugin params(cls=%r, datasource=%r,context=%r"
                  % (cls, datasource, context))
        return {}

    def __init__(self):
        super(GsSfaMetricPlugin, self).__init__()


    def prepTask(self, config):
        cmds = ('/opt/ddn/directmon/gridscaler/scripts/get_nsd_data.py',)
        for c in cmds:
            self.cmd.append(gsc.Cmd(command=c, template='metrics',
                                    config=self.config,
                                    parser=self.parseMetricResults))
        log.debug('XXX _prepMetricsCmd(): self.cmd = %r', self.cmd)

    def onSuccess(self, result, config):
        log.debug('XXXX onSuccess: values is %s', str(result))
        aggregate = self.new_data()
        events = []
        maps = []

        for k, v in result.items():
            alert = {}
            model = {'title': str(k),
                     'id': str('sfa_' + k),
                     'status': v['status']}
            maps.append(ObjectMap(data=model,
                                  modname=GSMODEL['sfaNodes']['modname']))
            if v['status'] != 'ready':
                alert['eventKey'] = k
                alert['severity'] = ZenEventClasses.Warning
                alert['summary'] = "Device is not in Ready State Actual" \
                                   " State is %s" % v['status']
                alert['component'] = k
                alert['eventClass'] = '/Perf/GridScalerV2/SFA'
                events.append(alert)

        rmap = RelationshipMap(relname=GSMODEL['sfaNodes']['relname'],
                               modname=GSMODEL['sfaNodes']['modname'],
                               objmaps=maps)

        aggregate['events'] = events
        aggregate['values'] = result
        aggregate['maps'] = [rmap]
        log.debug("Final Data : %s" % aggregate)
        return aggregate

    def onError(self, result, config):
        log.error("XXXX onError(self=%r, result=%r, config=%r)",
                  self, result.getErrorMessage(), config)
        aggregate = self.new_data()
        aggregate['events'] = [{
                                   'component': '',
                                   'device': config.id,
                                   'summary': 'error connection failed %s' %
                                              str(self.conn_params),
                                   'eventClass': '/Perf',
                                   'eventKey': '/Perf/GridScalerV2/SFA',
                                   'severity': ZenEventClasses.Error,
                               }]
        return aggregate

    def parseMetricResults(self, results, notused):
        """ parse the results for each datasource part of config """
        log.debug("XXX parseMetricResults called (config:%s, results: %s)",
                  self.config, results)
        res = None
        for ds in self.config.datasources:
            # the below template is available as part of ds.points.id
            if ds.template == 'GS_NsdDisk':  # Sfa Node
                res = gsu.GsSFAMetricParser(results, '')
            else:
                # unexpected, log an error and return none
                log.error('XXXX unexpected datasource %r', ds)
                continue

        log.debug('XXX result=%s', (str(res)))
        return res


class GsNsdMetricPlugin(DDNMetricPlugin):
    """This Class will collect metrics for nsd component"""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        log.debug("XXXX GsMetricPlugin params(cls=%r, datasource=%r,context=%r"
                  % (cls, datasource, context))
        return {}

    def __init__(self):
        super(GsNsdMetricPlugin, self).__init__()


    def prepTask(self, config):
        cmds = ('/opt/ddn/directmon/gridscaler/scripts/get_nodes_state.py',)
        for c in cmds:
            self.cmd.append(gsc.Cmd(command=c, template='metrics',
                                    config=self.config,
                                    parser=self.parseMetricResults))
        log.debug('XXX _prepMetricsCmd(): self.cmd = %r', self.cmd)

    def onSuccess(self, result, config):
        log.debug('XXXX NSD onSuccess: values is %s', str(result))
        result = gsu.dictflatten(result)
        aggregate = self.new_data()
        events = []
        maps = []
        values = {}

        for k, v in result.items():
            if str(k) in self.conn_params.get('nsdServers', ''):
                values[str(k)] = {'state': str(v)}
                alert = {}
                model = {'title': str(k),
                         'id': str('nsd_' + k),
                         'state': str(v)}
                maps.append(ObjectMap(data=model,
                                      modname=GSMODEL['nsdNodes']['modname']))
                if v != 'active':
                    alert['eventKey'] = str(k)
                    alert['severity'] = ZenEventClasses.Warning
                    alert['summary'] = str("Device is not in Active State"
                                           " Actual State is %s" % v)
                    alert['component'] = str(k)
                    alert['eventClass'] = '/Perf/GridscalerV2/NSD'
                    events.append(alert)
        rmap = RelationshipMap(relname=GSMODEL['nsdNodes']['relname'],
                               modname=GSMODEL['nsdNodes']['modname'],
                               objmaps=maps)

        aggregate['events'] = events
        aggregate['values'] = values
        aggregate['maps'] = [rmap]
        log.debug("Final Data : %s" % aggregate)
        return aggregate

    def onError(self, result, config):
        log.error("XXXX onError(self=%r, result=%r, config=%r)",
                  self, result.getErrorMessage(), config)
        aggregate = self.new_data()
        aggregate['events'] = [{
                                   'component': '',
                                   'device': config.id,
                                   'summary':
                                       'error connection failed %s'
                                       % str(self.conn_params),
                                   'eventClass': '/Perf',
                                   'eventKey': '/Perf/GridScalerV2/NSD',
                                   'severity': ZenEventClasses.Error,
                               }]
        return aggregate

    def parseMetricResults(self, results, notused):
        """ parse the results for each datasource part of config """
        log.debug("XXX parseMetricResults called (config:%s, results: %s)",
                  self.config, results)
        res = None
        for ds in self.config.datasources:
            # the below template is available as part of ds.points.id
            if ds.template == 'GS_NsdServer':  # Sfa Node
                res = gsu.gsNSDStats(results, '')
            else:
                # unexpected, log an error and return none
                log.error('XXXX unexpected datasource %r', ds)
                continue

        log.debug('XXX result=%s', (str(res)))
        return res


class GsCNMetricPlugin(DDNMetricPlugin):
    """This Class will collect metrics for Client Nodes component"""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        log.debug("XXXX GsMetricPlugin params(cls=%r, datasource=%r,context=%r"
                  % (cls, datasource, context))
        return {}

    def __init__(self):
        super(GsCNMetricPlugin, self).__init__()


    def prepTask(self, config):
        cmds = ('/opt/ddn/directmon/gridscaler/scripts/get_nodes_state.py',)
        for c in cmds:
            self.cmd.append(gsc.Cmd(command=c, template='metrics',
                                    config=self.config,
                                    parser=self.parseMetricResults))
        log.debug('XXX _prepMetricsCmd(): self.cmd = %r', self.cmd)

    def onSuccess(self, result, config):
        log.debug('XXXX CN onSuccess: values is %s', str(result))
        result = gsu.dictflatten(result)
        aggregate = self.new_data()
        events = []
        maps = []
        values = {}

        for k, v in result.items():
            if str(k) not in self.conn_params.get('nsdServers', ''):
                values[str(k)] = {'state': str(v)}
                alert = {}
                model = {'title': str(k),
                         'id': str('cn_' + k),
                         'state': str(v)}
                maps.append(ObjectMap(data=model,
                                      modname=GSMODEL['clientNodes']
                                      ['modname']))
                if v != 'active':
                    alert['eventKey'] = str(k)
                    alert['severity'] = ZenEventClasses.Warning
                    alert['summary'] = str("Device is not in Active"
                                           " State Actual State is %s" % v)
                    alert['component'] = str(k)
                    alert['eventClass'] = '/Perf/GridScalerV2/CN'
                    events.append(alert)
        rmap = RelationshipMap(relname=GSMODEL['clientNodes']['relname'],
                               modname=GSMODEL['clientNodes']['modname'],
                               objmaps=maps)

        aggregate['events'] = events
        aggregate['values'] = values
        aggregate['maps'] = [rmap]
        log.debug("Final Data : %s" % aggregate)
        return aggregate

    def onError(self, result, config):
        log.error("XXXX onError(self=%r, result=%r, config=%r)",
                  self, result.getErrorMessage(), config)
        aggregate = self.new_data()
        aggregate['events'] = [{
                                   'component': '',
                                   'device': config.id,
                                   'summary':
                                       'error connection failed %s'
                                       % str(self.conn_params),
                                   'eventClass': '/Perf',
                                   'eventKey': '/Perf/GridScalerV2/CN',
                                   'severity': ZenEventClasses.Error,
                               }]
        return aggregate

    def parseMetricResults(self, results, notused):
        """ parse the results for each datasource part of config """
        log.debug("XXX parseMetricResults called (config:%s, results: %s)",
                  self.config, results)
        res = None
        for ds in self.config.datasources:
            # the below template is available as part of ds.points.id

            if ds.template == 'GS_ClientNode':  # Sfa Node
                res = gsu.gsNSDStats(results, '')
            else:
                # unexpected, log an error and return none
                log.error('XXXX unexpected datasource %r', ds)
                continue

        log.debug('XXX result=%s', (str(res)))
        return res
