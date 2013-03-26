"""
Configuration files synchronizing
=====================
"""
from __future__ import with_statement

import yaml
from fabric.api import env
from fabric.contrib.files import upload_template
from fabtools.files import observe, read


def configs(filenames, callback=None):
    context_filename = 'contexts/%s.yaml' % env.target
    configs_changed = False
    with observe(context_filename) as context:
        context_data = yaml.load(read(context.filename))
        for filename in filenames:
            template_filename = '%s.template' % filename
            with observe(template_filename) as template:
                if context.changed or template.changed:
                    configs_changed = True
                    upload_template(template.filename, filename, context=context_data, use_sudo=True)
    if configs_changed and callback is not None:
        callback()
