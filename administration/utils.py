from django.apps import apps
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

site = admin.site


def _get_app_list(request):
    app_dict = {}
    user = request.user
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        print(model._meta)
        has_module_perms = user.has_module_perms(app_label)
        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            if True in perms.values():
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': apps.get_app_config(app_label).verbose_name,
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    return app_dict.values()

