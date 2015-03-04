import json
import logging
import collections
import re

log = logging.getLogger('zen.zengsutil')


def GsParser(results, key, log):
    """
        validates the given results dictionary using json.loads,
        if key it look for the key and give out a dictionary
    """
    try:
        jsonres = json.loads(results)
    except Exception as e:
        log.error('Json load failed for DATA: %s, ERROR: %s' % (results, e))
        return {}
    if key:
        return jsonres.get(key)
    return jsonres


def GsFsMetricsParser(results, key=''):
    """

    :param results:
    :param key:
    :return: returns fs_metrics data
    """
    fs_metrics = GsParser(results, '', log)
    if key:
        return fs_metrics.get(key)
    return fs_metrics


def gsNSDStats(results, key=''):
    """

    :param results:
    :param key:
    :return: returns NSD Metrics data
    """
    results = GsParser(results, '', log)
    return results


def dictflatten(dictres):
    """
        values in the given dict is converted in to string values
    """
    flatdict = {}
    for k, v in dictres.items():
        v = str(v)
        flatdict[k] = v
    return flatdict


def GsSFAMetricParser(results, key):
    """
    Gets sfa device metrics with status and returns sfa data
    """
    nsd_data = GsParser(results, 'nsdInfo', log)
    for k, v in nsd_data.items():
        tmp = nsd_data[k]
        stats = tmp['status']
        tmp.clear()
        tmp['status'] = stats
    return nsd_data


def GsSFAModelParser(results, key):
    """
    collect SFA model related information

    """
    nsd_data = GsParser(results, 'nsdInfo', log)
    if key:
        return nsd_data.get(key)
    return nsd_data


def GsNSDCollector(results, key=''):
    """
        Collect NSD model related information
    """
    results = GsParser(results, '', log)
    nsdlist = results.get('nsdServers', [])
    nsdinfo = [(nsd, {'Responsibility': get_responsibility(nsd, results),
                      'QuorumNode': is_quorumnode(nsd, results),
                      'secondaryServer': is_secServer(nsd, results)})
               for nsd in nsdlist]
    return dict(nsdinfo)


def GsFileSystemlistParser(results, fsid):
    fslist = GsParser(results, 'filesystems', log)
    if fsid:
        return fslist.get(fsid)
    return fslist


def GsCNCollector(results, key=''):
    """
        collect model related information for client nodes
    """
    results = GsParser(results, '', log)
    cnlist = results.get('clientNode', [])
    cninfo = [(nsd, {'Responsibility': get_responsibility(nsd, results),
                     'QuorumNode': is_quorumnode(nsd, results)})
              for nsd in cnlist]
    return dict(cninfo)


# parse results of nasctl vip_show
def GridNasVipParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for line in res.split('\n'):
        d = string_construct_repeat_counts(line)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(line) == d[line[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', line)
        tokens = line.split(':')
        if len(tokens) < 6:
            continue
        key = tokens[0].replace('/', '_')  # VIP -replace special chars with _
        model = {}
        model['id'] = key
        model['NetworkAddress'] = tokens[0].split('/')[0]
        model['NetworkMask'] = tokens[0].split('/')[1]
        model['ActiveNode'] = tokens[1]
        model['ActiveInterface'] = tokens[2]
        model['StandbyNode'] = str(tokens[5:])
        conf[key] = model
    log.debug('XXXX GridNasVipParse - returns %r', conf)
    return conf


# parse results of nasctl user_show
def GridNasUsersParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for oline in res.split('\n'):
        d = string_construct_repeat_counts(oline)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(oline) == d[oline[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', oline)
        line = line.strip(':')
        tokens = line.split(':')
        # pivot on an item which is an integer
        for pos, item in enumerate(tokens):
            if not item.isdigit():
                continue
            break
        else:
            # could not find valid reference to decode values
            # Skip this line
            log.debug('XXX skipping user info %s - cannot decode', oline)
            continue
        key = ' '.join(tokens[:pos])
        model = {}
        model['id'] = key
        model['title'] = key
        model['UID'] = tokens[pos]
        pos = pos + 1
        model['PrimaryGroup'] = ' '.join(tokens[pos:-1])
        model['Enabled'] = tokens[-1].strip()
        key = tokens[0].strip()
        conf[key] = model
    log.debug('XXXX GridNasUsersParse - returns %r', conf)
    return conf


# parse results of nasctl share_show
def GridNasNetworkShareParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for line in res.split('\n'):
        d = string_construct_repeat_counts(line)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(line) == d[line[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', line)
        line = line.strip(':')
        tokens = line.split(':')
        if len(tokens) < 3:
            continue
        key = tokens[0].strip()
        model = {}
        model['id'] = key
        model['title'] = key
        model['Path'] = tokens[1].strip()
        model['Options'] = ','.join(tokens[2:])
        conf[key] = model
    log.debug('XXXX GridNasNetworkShareParse - returns %r', conf)
    return conf


# parse results of nasctl nfs_show
def GridNasNFSParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for line in res.split('\n'):
        d = string_construct_repeat_counts(line)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(line) == d[line[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', line)
        line = line.strip(':')
        tokens = line.split(':')
        if len(tokens) < 3:
            continue
        key = tokens[0].strip()
        model = {}
        model['id'] = key
        model['NetworkAddress'] = tokens[1].strip()
        model['Status'] = tokens[2].strip()
        conf[key] = model
    log.debug('XXXX GridNasNFSParse - returns %r', conf)
    return conf


# parse results of nasctl group_show
def GridNasGroupsParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for oline in res.split('\n'):
        d = string_construct_repeat_counts(oline)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(oline) == d[oline[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', oline)
        line = line.strip(':')
        tokens = line.split(':')
        for pos, item in enumerate(tokens):
            if not item.isdigit():
                continue
            break
        else:
            # could not find valid reference to decode values
            # Skip this line
            log.debug('XXX skipping group %s - cannot decode', oline)
            continue
        key = ' '.join(tokens[:pos])
        model = {}
        model['id'] = key
        model['title'] = key
        model['GID'] = tokens[pos]
        pos = pos + 1
        model['Domain'] = ' '.join(tokens[pos:])
        conf[key] = model
    log.debug('XXXX GridNasGroupsParse - returns %r', conf)
    return conf


# parse results of nasctl cifs_show
def GridNasCIFSParse(results, notused):
    conf = {}
    res = results.strip('\n')  # Strip leading/trailing newlines
    stripped = False
    for line in res.split('\n'):
        d = string_construct_repeat_counts(line)
        if not stripped:
            # strip all output till a line is found which is only '-'s
            if len(line) == d[line[0]]:
                stripped = True
            continue
        line = re.sub('\s+', ':', line)
        line = line.strip(':')
        tokens = line.split(':')
        if len(tokens) < 4:
            continue
        key = tokens[0].strip()
        model = {}
        model['id'] = key
        model['NetworkAddress'] = tokens[1].strip()
        model['Status'] = tokens[2].strip()
        if tokens[3].strip() == 'No':
            model['ADStatus'] = 'Not Joined'
        elif tokens[3].strip() == 'Yes':
            model['ADStatus'] = 'Joined'
        else:
            model['ADStatus'] = tokens[3].strip()

        conf[key] = model
    log.debug('XXXX GridNasCIFSParse - returns %r', conf)
    return conf


def get_responsibility(node, jres):
    if node == jres.get('clusterManager', ''):
        return 'clusterManager'
    elif node in jres['managers']:
        return 'manager'
    else:
        return None


def is_quorumnode(node, jres):
    if node in jres['quorumNodes']:
        return 'Yes'
    return 'no'


def is_secServer(node, jres):
    if node == jres.get('secondaryServer', ''):
        return 'Yes'
    return 'no'


def string_construct_repeat_counts(s):
    d = collections.defaultdict(int)
    for c in s:
        d[c] += 1
    return d
