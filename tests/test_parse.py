# -*- coding: utf-8 -*-
# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from io import StringIO

from marabunta.parser import YamlParser, YAML_EXAMPLE


MALFORMED_YAML_EXAMPLE = u"""
migration:
  options:
    # --workers=0 --stop-after-init are automatically added
    install_command: odoo
    install_args: --log-level=debug
    backup:
      command: echo "backup command on $database $db_user $db_password $db_host $db_port"
      stop_on_failure: true
      ignore_if: test "${RUNNING_ENV}" != "prod"
  versions:
    - version: setup
      operations:
        pre:  # executed before 'addons'
          - echo 'pre-operation'
        post:  # executed after 'addons'
          - anthem songs::install
      addons:
        upgrade:  # executed as odoo --stop-after-init -i/-u ...
          - base
          - document
        # remove:  # uninstalled with a python script
      modes:
        prod:
          operations:
            pre:
              - echo 'pre-operation executed only when the mode is prod'
            post:
              - anthem songs::load_production_data
        demo:
          operations:
            post:
              - anthem songs::load_demo_data
          addons:
            upgrade:
              - demo_addon
      operations:
        pre:
          - echo 'Duplicated operations step'
"""  # noqa


def test_parse_yaml_example():
    file_example = StringIO(YAML_EXAMPLE)
    parser = YamlParser.parser_from_buffer(file_example)
    import pdb; pdb.set_trace()
    migration = parser.parse()
    assert len(migration.versions) == 4


def test_parse_malformed_yaml():
    malformed = StringIO(MALFORMED_YAML_EXAMPLE)
    parser = YamlParser.parser_from_buffer(malformed)
    import pdb; pdb.set_trace()
    migration = parser.parse()
