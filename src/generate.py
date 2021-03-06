#!/usr/bin/env python

import os
import string
import subprocess
import sys
import tempfile

current_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.normpath(current_dir + '/../resources/') + '/'

puppet_types = [line.strip() for line in open(resource_dir + 'typelist.txt')]
puppet_types.sort()

f = open(resource_dir + 'parameters.tmpl')
parameter_tmpl = string.Template(f.read())
f.close()

f = open(resource_dir + 'createblock.tmpl')
typedef_tmpl = string.Template(f.read())
f.close()

f = open(resource_dir + 'header.tmpl')
hieratic_class = f.read()
f.close()

hieratic_class += """\nclass hieratic (
  $global_enable = true,
  $prefix = '',
  $firewall_label = 'firewall',
  $firewall_enabled = false,
  $firewall_defaults = {},
  $firewall_pre_label = 'firewall_pre',
  $firewall_pre_enabled = false,
  $firewall_pre_defaults = {},
  $firewall_post_label = 'firewall_post',
  $firewall_post_enabled = false,
  $firewall_post_defaults = {},
  $class_label =
    'class',
  $class_defaults = {},
  $class_enabled = false,
"""

for puppet_type in puppet_types:
  hieratic_class += parameter_tmpl.substitute(type=puppet_type, type_delimited=puppet_type.replace('::', '_'))

hieratic_class += ") {\n\n"

for puppet_type in puppet_types:
  hieratic_class += typedef_tmpl.substitute(type=puppet_type, type_delimited=puppet_type.replace('::', '_')) + "\n"

hieratic_class += """

  if($class_enabled or $global_enable) {
    $class_config =
      hiera_hash("${prefix}${class_label}",
        $class_defaults)

    create_resources('class',
      $class_config)
  }

  class { 'hieratic::firewall':
    global_enable          => $global_enable,
    firewall_label         => "${prefix}${firewall_label}",
    firewall_enabled       => $firewall_enabled,
    firewall_defaults      => $firewall_defaults,
    firewall_pre_label     => "${prefix}${firewall_pre_label}",
    firewall_pre_enabled   => $firewall_pre_enabled,
    firewall_pre_defaults  => $firewall_pre_defaults,
    firewall_post_label    => "${prefix}${firewall_post_label}",
    firewall_post_enabled  => $firewall_post_enabled,
    firewall_post_defaults => $firewall_post_defaults,
  }

}"""


# puppet-lint only works on files, so we write it to temp and return the result.
#f = tempfile.NamedTemporaryFile()
#f.write(hieratic_class)
#devnull = open(os.devnull, 'w')
#subprocess.call(['puppet-lint',f.name,'--fix'], stdout=devnull, stderr=devnull )
#f.seek(0)
#hieratic_class = f.read()
#f.close()


print hieratic_class
