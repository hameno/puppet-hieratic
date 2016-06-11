# == Class: hieratic
#
# Internal class- this should be called through Hieratic, not directly.
#
# === Authors
#
# Robert Hafner <tedivm@tedivm.com>
#
# === Copyright
#
# Copyright 2015 Robert Hafner
#

class hieratic::firewall (
  $global_enable = true,
  $firewall_label = firewall,
  $firewall_enabled = false,
  $firewall_defaults = { },
  $firewall_pre_label = firewall_pre,
  $firewall_pre_enabled = false,
  $firewall_pre_defaults = { },
  $firewall_post_label = firewall_post,
  $firewall_post_enabled = false,
  $firewall_post_defaults = { },
) {

  if(defined('firewall')
  and ($firewall_enabled or $global_enable)) {

    # do NOT use the resource { "firewall": purge => true } chunk
    resources { 'firewall':
      purge => false
    }

    # Globally set firewallchains as purged by default:
    firewallchain {
      [ "PREROUTING:mangle:IPv4",
        "FORWARD:filter:IPv4",
        "FORWARD:mangle:IPv4",
        "POSTROUTING:mangle:IPv4",
        "INPUT:filter:IPv4",
        "OUTPUT:filter:IPv4",
        "INPUT:mangle:IPv4",
        "OUTPUT:mangle:IPv4", ]:
        purge => true
    }
    # Don't purge the fail2ban-ssh chain itself...
    firewallchain { 'fail2ban-ssh:filter:IPv4':
      purge => false
    }

    Firewall {
      before  => Class['hieratic::firewall::post'],
      require => Class['hieratic::firewall::pre'],
    }

    $firewall_config = hiera_hash($firewall_label, { })
    create_resources(firewall, $firewall_config, $firewall_defaults)

    class { ['hieratic::firewall::pre', 'hieratic::firewall::post']: }
  }
}
