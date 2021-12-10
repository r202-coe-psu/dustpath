import datetime

from . import (
    main,
    dashboard,
    users,
    maps,
    compile,
    )


def add_date_url(url):
    now = datetime.datetime.now()
    return f'{url}?date={now.strftime("%Y%m%d")}'


def get_subblueprints(views=[]):
    blueprints = []
    for view in views:
        blueprints.append(view.module)

        if "subviews" in dir(view):
            for module in get_subblueprints(view.subviews):
                if view.module.url_prefix and module.url_prefix:
                    module.url_prefix = view.module.url_prefix + module.url_prefix
                blueprints.append(module)

    return blueprints


def register_blueprint(app):
    app.add_template_filter(add_date_url)
    blueprints = get_subblueprints(
        [
            main,
            dashboard,
            users,
            maps,
            compile,
        ])

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
