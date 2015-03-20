class hieratic::firewall (
  $global_enable = true,
  $firewall_label = firewall,
  $firewall_enabled = false,
  $firewall_pre_label = firewall_pre,
  $firewall_pre_enabled = false,
  $firewall_post_label = firewall_post,
  $firewall_post_enabled = false,
) {

  if(defined('firewall') and ($firewall_enabled or $global_enable)) {
    resources { "firewall":
      purge => true
    }

    Firewall {
      before  => Class['fw::post'],
      require => Class['fw::pre'],
    }

    $firewall_config = hiera_hash($firewall_label, {})
    create_resources(firewall, $firewall_config)

    class { ['fw::pre', 'fw::post']: }
  }
}