# Copyright 2015 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

DEFAULT_GROUP_NAME = "DEFAULT"
# The scheduler has options in several groups
METRICS_GROUP_NAME = "metrics"
TRUSTED_GROUP_NAME = "trusted_computing"
UPGRADE_GROUP_NAME = "upgrade_levels"


host_subset_size_opt = cfg.IntOpt("scheduler_host_subset_size",
        default=1,
        help="""
New instances will be scheduled on a host chosen randomly from a subset of the
N best hosts, where N is the value set by this option.  Valid values are 1 or
greater. Any value less than one will be treated as 1.

Setting this to a value greater than 1 will reduce the chance that multiple
scheduler processes handling similar requests will select the same host,
creating a potential race condition. By selecting a host randomly from the N
hosts that best fit the request, the chance of a conflict is reduced. However,
the higher you set this value, the less optimal the chosen host may be for a
given request.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    None
""")

bm_default_filter_opt = cfg.ListOpt("baremetal_scheduler_default_filters",
        default=[
            "RetryFilter",
            "AvailabilityZoneFilter",
            "ComputeFilter",
            "ComputeCapabilitiesFilter",
            "ImagePropertiesFilter",
            "ExactRamFilter",
            "ExactDiskFilter",
            "ExactCoreFilter",
        ],
        help="""
This option specifies the filters used for filtering baremetal hosts. The value
should be a list of strings, with each string being the name of a filter class
to be used. When used, they will be applied in order, so place your most
restrictive filters first to make the filtering process more efficient.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    If the 'scheduler_use_baremetal_filters' option is False, this option has
    no effect.
""")

use_bm_filters_opt = cfg.BoolOpt("scheduler_use_baremetal_filters",
        default=False,
        help="""
Set this to True to tell the nova scheduler that it should use the filters
specified in the 'baremetal_scheduler_default_filters' option. If you are not
scheduling baremetal nodes, leave this at the default setting of False.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    If this option is set to True, then the filters specified in the
    'baremetal_scheduler_default_filters' are used instead of the filters
    specified in 'scheduler_default_filters'.
""")

host_mgr_avail_filt_opt = cfg.MultiStrOpt("scheduler_available_filters",
        default=["nova.scheduler.filters.all_filters"],
        help="""
This is an unordered list of the filter classes the Nova scheduler may apply.
Only the filters specified in the 'scheduler_default_filters' option will be
used, but any filter appearing in that option must also be included in this
list.

By default, this is set to all filters that are included with Nova. If you wish
to change this, replace this with a list of strings, where each element is the
path to a filter.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    scheduler_default_filters
""")

host_mgr_default_filt_opt = cfg.ListOpt("scheduler_default_filters",
        default=[
          "RetryFilter",
          "AvailabilityZoneFilter",
          "RamFilter",
          "DiskFilter",
          "ComputeFilter",
          "ComputeCapabilitiesFilter",
          "ImagePropertiesFilter",
          "ServerGroupAntiAffinityFilter",
          "ServerGroupAffinityFilter",
          ],
        help="""
This option is the list of filter class names that will be used for filtering
hosts. The use of 'default' in the name of this option implies that other
filters may sometimes be used, but that is not the case. These filters will be
applied in the order they are listed, so place your most restrictive filters
first to make the filtering process more efficient.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    All of the filters in this option *must* be present in the
    'scheduler_available_filters' option, or a SchedulerHostFilterNotFound
    exception will be raised.
""")

host_mgr_sched_wgt_cls_opt = cfg.ListOpt("scheduler_weight_classes",
        default=["nova.scheduler.weights.all_weighers"],
        help="""
This is a list of weigher class names. Only hosts which pass the filters are
weighed. The weight for any host starts at 0, and the weighers order these
hosts by adding to or subtracting from the weight assigned by the previous
weigher. Weights may become negative.

An instance will be scheduled to one of the N most-weighted hosts, where N is
'scheduler_host_subset_size'.

By default, this is set to all weighers that are included with Nova. If you
wish to change this, replace this with a list of strings, where each element is
the path to a weigher.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    None
""")

host_mgr_tracks_inst_chg_opt = cfg.BoolOpt("scheduler_tracks_instance_changes",
        default=True,
        help="""
The scheduler may need information about the instances on a host in order to
evaluate its filters and weighers. The most common need for this information is
for the (anti-)affinity filters, which need to choose a host based on the
instances already running on a host.

If the configured filters and weighers do not need this information, disabling
this option will improve performance. It may also be disabled when the tracking
overhead proves too heavy, although this will cause classes requiring host
usage data to query the database on each request instead.

This option is only used by the FilterScheduler and its subclasses; if you use
a different scheduler, this option has no effect.

* Services that use this:

    ``nova-scheduler``

* Related options:

    None
""")

rpc_sched_topic_opt = cfg.StrOpt("scheduler_topic",
        default="scheduler",
        help="""
This is the message queue topic that the scheduler 'listens' on. It is used
when the scheduler service is started up to configure the queue, and whenever
an RPC call to the scheduler is made. There is almost never any reason to ever
change this value.

* Services that use this:

    ``nova-scheduler``

* Related options:

    None
""")

scheduler_json_config_location_opt = cfg.StrOpt(
        "scheduler_json_config_location",
        default="",
        help="""
The absolute path to the scheduler configuration JSON file, if any. This file
location is monitored by the scheduler for changes and reloads it if needed. It
is converted from JSON to a Python data structure, and passed into the
filtering and weighing functions of the scheduler, which can use it for dynamic
configuration.

* Services that use this:

    ``nova-scheduler``

* Related options:

    None
""")

sched_driver_host_mgr_opt = cfg.StrOpt("scheduler_host_manager",
        default="nova.scheduler.host_manager.HostManager",
        help="The scheduler host manager class to use")

driver_opt = cfg.StrOpt("scheduler_driver",
        default="nova.scheduler.filter_scheduler.FilterScheduler",
        help="Default driver to use for the scheduler")

driver_period_opt = cfg.IntOpt("scheduler_driver_task_period",
        default=60,
        help="How often (in seconds) to run periodic tasks in the scheduler "
             "driver of your choice. Please note this is likely to interact "
             "with the value of service_down_time, but exactly how they "
             "interact will depend on your choice of scheduler driver.")

disk_allocation_ratio_opt = cfg.FloatOpt("disk_allocation_ratio",
        default=1.0,
        help="Virtual disk to physical disk allocation ratio")

isolated_img_opt = cfg.ListOpt("isolated_images",
        default=[],
        help="Images to run on isolated host")

isolated_host_opt = cfg.ListOpt("isolated_hosts",
        default=[],
        help="Host reserved for specific images")

restrict_iso_host_img_opt = cfg.BoolOpt(
        "restrict_isolated_hosts_to_isolated_images",
        default=True,
        help="Whether to force isolated hosts to run only isolated images")

# This option specifies an option group, so register separately
rpcapi_cap_opt = cfg.StrOpt("scheduler",
        help="Set a version cap for messages sent to scheduler services")

# These opts are registered as a separate OptGroup
trusted_opts = [
    cfg.StrOpt("attestation_server",
            help="Attestation server HTTP"),
    cfg.StrOpt("attestation_server_ca_file",
            help="Attestation server Cert file for Identity verification"),
    cfg.StrOpt("attestation_port",
            default="8443",
            help="Attestation server port"),
    cfg.StrOpt("attestation_api_url",
            default="/OpenAttestationWebServices/V1.0",
            help="Attestation web API URL"),
    cfg.StrOpt("attestation_auth_blob",
            help="Attestation authorization blob - must change"),
    cfg.IntOpt("attestation_auth_timeout",
            default=60,
            help="Attestation status cache valid period length"),
    cfg.BoolOpt("attestation_insecure_ssl",
            default=False,
            help="Disable SSL cert verification for Attestation service")
]

max_io_ops_per_host_opt = cfg.IntOpt("max_io_ops_per_host",
        default=8,
        help="Tells filters to ignore hosts that have this many or more "
             "instances currently in build, resize, snapshot, migrate, rescue "
             "or unshelve task states")

agg_img_prop_iso_namespace_opt = cfg.StrOpt(
        "aggregate_image_properties_isolation_namespace",
        help="Force the filter to consider only keys matching the given "
             "namespace.")

agg_img_prop_iso_separator_opt = cfg.StrOpt(
        "aggregate_image_properties_isolation_separator",
        default=".",
        help="The separator used between the namespace and keys")

max_instances_per_host_opt = cfg.IntOpt("max_instances_per_host",
        default=50,
        help="Ignore hosts that have too many instances")

ram_weight_mult_opt = cfg.FloatOpt("ram_weight_multiplier",
        default=1.0,
        help="Multiplier used for weighing ram. Negative numbers mean to "
             "stack vs spread.")

io_ops_weight_mult_opt = cfg.FloatOpt("io_ops_weight_multiplier",
        default=-1.0,
        help="Multiplier used for weighing host io ops. Negative numbers mean "
             "a preference to choose light workload compute hosts.")

# These opts are registered as a separate OptGroup
metrics_weight_opts = [
     cfg.FloatOpt("weight_multiplier",
            default=1.0,
            help="Multiplier used for weighing metrics."),
     cfg.ListOpt("weight_setting",
            default=[],
            help="How the metrics are going to be weighed. This should be in "
                 "the form of '<name1>=<ratio1>, <name2>=<ratio2>, ...', "
                 "where <nameX> is one of the metrics to be weighed, and "
                 "<ratioX> is the corresponding ratio. So for "
                 "'name1=1.0, name2=-1.0' The final weight would be "
                 "name1.value * 1.0 + name2.value * -1.0."),
    cfg.BoolOpt("required",
            default=True,
            help="How to treat the unavailable metrics. When a metric is NOT "
                 "available for a host, if it is set to be True, it would "
                 "raise an exception, so it is recommended to use the "
                 "scheduler filter MetricFilter to filter out those hosts. If "
                 "it is set to be False, the unavailable metric would be "
                 "treated as a negative factor in weighing process, the "
                 "returned value would be set by the option "
                 "weight_of_unavailable."),
    cfg.FloatOpt("weight_of_unavailable",
            default=float(-10000.0),
            help="The final weight value to be returned if required is set to "
                 "False and any one of the metrics set by weight_setting is "
                 "unavailable."),
]

scheduler_max_att_opt = cfg.IntOpt("scheduler_max_attempts",
            default=3,
            min=1,
            help="Maximum number of attempts to schedule an instance")

soft_affinity_weight_opt = cfg.FloatOpt('soft_affinity_weight_multiplier',
            default=1.0,
            help='Multiplier used for weighing hosts '
                 'for group soft-affinity. Only a '
                 'positive value is meaningful. Negative '
                 'means that the behavior will change to '
                 'the opposite, which is soft-anti-affinity.')

soft_anti_affinity_weight_opt = cfg.FloatOpt(
    'soft_anti_affinity_weight_multiplier',
                 default=1.0,
                 help='Multiplier used for weighing hosts '
                      'for group soft-anti-affinity. Only a '
                      'positive value is meaningful. Negative '
                      'means that the behavior will change to '
                      'the opposite, which is soft-affinity.')


default_opts = [host_subset_size_opt,
               bm_default_filter_opt,
               use_bm_filters_opt,
               host_mgr_avail_filt_opt,
               host_mgr_default_filt_opt,
               host_mgr_sched_wgt_cls_opt,
               host_mgr_tracks_inst_chg_opt,
               rpc_sched_topic_opt,
               sched_driver_host_mgr_opt,
               driver_opt,
               driver_period_opt,
               scheduler_json_config_location_opt,
               disk_allocation_ratio_opt,
               isolated_img_opt,
               isolated_host_opt,
               restrict_iso_host_img_opt,
               max_io_ops_per_host_opt,
               agg_img_prop_iso_namespace_opt,
               agg_img_prop_iso_separator_opt,
               max_instances_per_host_opt,
               ram_weight_mult_opt,
               io_ops_weight_mult_opt,
               scheduler_max_att_opt,
               soft_affinity_weight_opt,
               soft_anti_affinity_weight_opt,
              ]


def register_opts(conf):
    conf.register_opts(default_opts)
    conf.register_opt(rpcapi_cap_opt, UPGRADE_GROUP_NAME)
    trust_group = cfg.OptGroup(name=TRUSTED_GROUP_NAME,
                               title="Trust parameters")
    conf.register_group(trust_group)
    conf.register_opts(trusted_opts, group=trust_group)
    conf.register_opts(metrics_weight_opts, group=METRICS_GROUP_NAME)


def list_opts():
    return {DEFAULT_GROUP_NAME: default_opts,
            UPGRADE_GROUP_NAME: [rpcapi_cap_opt],
            TRUSTED_GROUP_NAME: trusted_opts,
            METRICS_GROUP_NAME: metrics_weight_opts,
            }
