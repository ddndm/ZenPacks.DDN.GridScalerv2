# Import zenpacklib from the current directory (zenpacklib.py).
from . import zenpacklib


# Create a ZenPackSpec and name it CFG.
CFG = zenpacklib.ZenPackSpec(
    name=__name__,

    zProperties={
        'DEFAULTS': {'category': 'DDN GridScaler Solution'},

        'zGSNSDList': {
            'type': 'string',
        },
    },

    classes={
        'GridScalerV2Device': {
            'base': zenpacklib.Device,
            'label': 'GridScalerV2Device',

            'properties': {
                'clusterManager': {
                    'label': 'clusterManager',
                    'order': 4.2,
                },
                'domain': {
                    'label': 'cluster Domain',
                    'order': 4.3,
                },
                'fileCopyCMD': {
                    'label': 'fileCopyCMD',
                    'order': 4.4,
                },
                'gpfsVersion': {
                    'label': 'gpfsVersion',
                    'order': 4.5,
                },
                'numActiveClientNodes': {
                    'label': 'numActiveClientNodes',
                    'order': 4.6,
                },
                'numClientNodes': {
                    'label': 'numClientNodes',
                    'order': 4.7,
                },
                'numFs': {
                    'label': 'numFs',
                    'order': 4.8,
                },
                'numLocalNodesActive': {
                    'label': 'numLocalNodesActive',
                    'order': 4.9,
                },
                'numManagerNodes': {
                    'label': 'numManagerNodes',
                    'order': 4.10,
                },
                'numNSDNodes': {
                    'label': 'numNSDNodes',
                    'order': 4.11,
                },
                'numQuorumNodesActive': {
                    'label': 'numQuorumNodesActive',
                    'order': 4.12,
                },
                'numQuorumNodesDefined': {
                    'label': 'numQuorumNodesDefined',
                    'order': 4.13,
                },
                'numRemoteNodesJoined': {
                    'label': 'numRemoteNodesJoined',
                    'order': 4.14,
                },
                'primaryHost': {
                    'label': 'primaryHost',
                    'order': 4.15,
                },
                'quorumState': {
                    'label': 'quorumState',
                    'order': 4.16,
                },
                'secondaryHost': {
                    'label': 'secondaryHost',
                    'order': 4.17,
                },
                'totalMounts': {
                    'label': 'totalMounts',
                    'order': 4.18,
                },

                'config': {
                    'label': 'config',
                },

                'numNodesDefined': {
                    'label': 'numNodesDefined',
                },

                'shellCMD': {
                    'label': 'shellCMD',
                },

                'numNSD': {
                    'label': 'numNSD',
                },

                'preferredNSD': {
                    'label': 'Preferred Target',
                    'order': 4.19,
                },
                'networkNSDs': {
                    'label': 'nsd Network Targets',
                    'order': 4.20,
                },
                'nsdServers': {
                    'label': 'NsdServers',
                    'order': 4.20,
                },
            }
        },

        'ClientNode': {
            'base': zenpacklib.Component,
            'label': 'GS_ClientNode',
            'order': 1.4,
            'properties': {
                'Responsibility': {
                    'label': 'Responsibility',
                    'order': 4.0,
                },

                'QuorumNode': {
                    'label': 'QuorumNode',
                    'order': 4.1,
                },
                'state': {
                    'label': 'State',
                    'order': 4.3,
                },
            }
        },

        'NsdNode': {
            'base': zenpacklib.Component,
            'meta_type': 'NsdNode',
            'label': 'GS_NsdServer',
            'order': 1.2,
            'properties': {
                'Responsibility': {
                    'label': 'Responsibility',
                    'order': 4.0,
                },

                'QuorumNode': {
                    'label': 'QuorumNode',
                    'order': 4.1,
                },
                'state': {
                    'label': 'State',
                    'order': 4.3,
                },
                'secondaryServer': {
                    'label': 'SecondaryServer',
                    'order': 4.2,
                },
                'sfaNode': {
                    'label': 'Sfa Node',
                    'order': 4.15,
                    'type_': 'entity',
                }
            }
        },

        'SfaNode': {
            'base': zenpacklib.Component,
            'meta_type': 'SfaNode',
            'label': 'GS_NsdDisk',
            'order': 1.3,
            'properties': {
                'status': {
                    'label': 'Status',
                    'order': 4.0,
                },

                'sectorSize': {
                    'label': 'Sector Size',
                    'order': 4.1,
                },

                'filesystem': {
                    'label': 'FileSystem',
                    'order': 4.3,
                },

                'failureGroup': {
                    'label': 'Failure Group',
                    'order': 4.4,
                },

                'holdMeta': {
                    'label': 'hold Meta',
                    'order': 4.5,
                },

                'ioNode': {
                    'label': 'ioNode',
                    'order': 4.9,
                },
                'nsdServers': {
                    'label': 'nsdServers',
                    'order': 4.10,
                },
                'storagePool': {
                    'label': 'storagePool',
                    'order': 4.11,
                },
                'holdData': {
                    'label': 'holdData',
                    'order': 4.12,
                },
                'type': {
                    'label': 'type',
                    'order': 4.13,
                },
                'availability': {
                    'label': 'availability',
                    'order': 4.14,
                },
                'nsdNode': {
                    'label': 'Nsd Node',
                    'order': 4.15,
                    'type_': 'entity',
                }
            }
        },

        'FsList': {
            'base': zenpacklib.Component,
            'label': 'GS_FsList',
            'order': 1.1,
            'properties': {

                'logFileSize': {
                    'order': 4.1,
                    'label': 'logFileSize'
                },
                'filesets': {
                    'order': 4.2,
                    'label': 'filesets'
                },
                'mountPriority': {
                    'order': 4.3,
                    'label': 'mountPriority'
                },
                'inodeSize': {
                    'order': 4.4,
                    'label': 'inodeSize'
                },
                'blockSize': {
                    'order': 4.5,
                    'label': 'blockSize'
                },
                'aclSemantics': {
                    'order': 4.6,
                    'label': 'aclSemantics'
                },
                'defaultMountPoint': {
                    'order': 4.7,
                    'label': 'defaultMountPoint'
                },
                'filesetdfEnabled': {
                    'order': 4.8,
                    'label': 'filesetdfEnabled'
                },
                'version': {
                    'order': 4.9,
                    'label': 'version'
                },
                'diskStoragePools': {
                    'order': 4.10,
                    'label': 'diskStoragePools'
                },
                'indirectBlockSize': {
                    'order': 4.11,
                    'label': 'indirectBlockSize'
                },

                'additionalMountOpts': {
                    'order': 4.12,
                    'label': 'additionalMountOpts'
                },
                'mtimeMountEnabled': {
                    'order': 4.13,
                    'label': 'mtimeMountEnabled'
                },
                'strictReplicaAlloc': {
                    'order': 4.14,
                    'label': 'strictReplicaAlloc'
                },
                'defaultDataReplicas': {
                    'order': 4.15,
                    'label': 'defaultDataReplicas'
                },
                'manager': {
                    'order': 4.16,
                    'label': 'manager'
                },
                'estimateMountNodes': {
                    'order': 4.17,
                    'label': 'estimateMountNodes'
                },
                'quotasEnforced': {
                    'order': 4.18,
                    'label': 'quotasEnforced'
                },
                'mountedOnNodes': {
                    'order': 4.19,
                    'label': 'mountedOnNodes'
                },
                'nsds': {
                    'order': 4.20,
                    'label': 'nsds'
                },
                'supportLargeLuns': {
                    'order': 4.21,
                    'label': 'supportLargeLuns'
                },
                'blockAllocType': {
                    'order': 4.23,
                    'label': 'blockAllocType'
                },
                'defaultMetaReplicas': {
                    'order': 4.24,
                    'label': 'defaultMetaReplicas'
                },
                'fastExtAttEnabled': {
                    'order': 4.25,
                    'label': 'fastExtAttEnabled'
                },
                'minimumFragSize': {
                    'order': 4.26,
                    'label': 'minimumFragSize'
                },
                'autoMount': {
                    'order': 4.27,
                    'label': 'autoMount'
                },
                'maxDataReplicas': {
                    'order': 4.28,
                    'label': 'maxDataReplicas'
                },
                'createTime': {
                    'order': 4.29,
                    'label': 'createTime'
                },
                'defaultQuotasEnabled': {
                    'order': 4.30,
                    'label': 'defaultQuotasEnabled'
                },
                'fileLockingSemantic': {
                    'order': 4.31,
                    'label': 'fileLockingSemantic'
                },
                'perFilesetQuotaEnforced': {
                    'order': 4.32,
                    'label': 'perFilesetQuotaEnforced'
                },
                'dmApiEnabled': {
                    'order': 4.33,
                    'label': 'dmApiEnabled'
                },
                'maxMetaReplicas': {
                    'order': 4.34,
                    'label': 'maxMetaReplicas'
                },
                'maxInodes': {
                    'order': 4.35,
                    'label': 'maxInodes'
                },
                'suppressAtimeMountEnabled': {
                    'order': 4.36,
                    'label': 'suppressAtimeMountEnabled'
                },
                'defaultGraceTime': {
                    'order': 4.37,
                    'label': 'defaultGraceTime'
                },
                'defaultQuota': {
                    'order': 4.38,
                    'label': 'defaultQuota'
                },
                'defaultQuotaStatus': {
                    'order': 4.39,
                    'label': 'defaultQuotaStatus'
                },

            }
        },

        # GridNAS Entries

        'VirtualNetwork': {
            'base': zenpacklib.Component,
            'label': 'GNAS_VirtualNetwork',
            'order': 2.2,
            'properties': {
                'NetworkAddress': {
                    'label': 'Network Address',
                    'order': 4.0,
                },
                'NetworkMask': {
                    'label': 'Network Mask',
                    'order': 4.1,
                },
                'ActiveNode': {
                    'label': 'ActiveNode',
                    'order': 4.2,
                },
                'ActiveInterface': {
                    'label': 'ActiveInterface',
                    'order': 4.3,
                },
                'StandbyNode': {
                    'label': 'StandbyNode',
                    'order': 4.4,
                },
            },
        },

        'CIFS': {
            'base': zenpacklib.Component,
            'label': 'GNAS_CIFS',
            'order': 2.3,
            'properties': {
                'NetworkAddress': {
                    'label': 'Network Address',
                    'order': 4.0,
                },
                'Status': {
                    'label': 'Status',
                    'order': 4.1,
                },
                'ADStatus': {
                    'label': 'ActiveDirectoryStatus',
                    'order': 4.2,
                },
            },
        },

        'NFS': {
            'base': zenpacklib.Component,
            'label': 'GNAS_NFS',
            'order': 2.4,
            'properties': {
                'NetworkAddress': {
                    'label': 'Network Address',
                    'order': 4.0,
                },
                'Status': {
                    'label': 'Status',
                    'order': 4.1,
                },
            },
        },

        'NetworkShare': {
            'base': zenpacklib.Component,
            'label': 'GNAS_NetworkShare',
            'order': 2.1,
            'properties': {
                'Path': {
                    'label': 'Path',
                    'order': 4.0,
                },
                'Options': {
                    'label': 'Options',
                    'order': 4.1,
                },
            },
        },

        'NasUser': {
            'base': zenpacklib.Component,
            'label': 'GNAS_NasUser',
            'order': 2.5,
            'properties': {
                'UID': {
                    'label': 'UID',
                    'order': 4.0,
                },
                'PrimaryGroup': {
                    'label': 'Primary Group',
                    'order': 4.1,
                },
                'Enabled': {
                    'label': 'Enabled',
                    'order': 4.2,
                },
            },
        },

        'NasGroup': {
            'base': zenpacklib.Component,
            'label': 'GNAS_NasGroup',
            'order': 2.6,
            'properties': {
                'GID': {
                    'label': 'GID',
                    'order': 4.0,
                },
                'Domain': {
                    'label': 'Domain',
                    'order': 4.1,
                },
            },
        },
    },

    class_relationships=zenpacklib.relationships_from_yuml(
        """[GridScalerV2Device]++-[ClientNode]
           [GridScalerV2Device]++-[NsdNode]
           [GridScalerV2Device]++-[SfaNode]
           [GridScalerV2Device]++-[FsList]
           [GridScalerV2Device]++-[CIFS]
           [GridScalerV2Device]++-[NFS]
           [GridScalerV2Device]++-[NetworkShare]
           [GridScalerV2Device]++-[NasUser]
           [GridScalerV2Device]++-[NasGroup]
           [GridScalerV2Device]++-[VirtualNetwork]"""
    )
)

# Create the specification.
CFG.create()
