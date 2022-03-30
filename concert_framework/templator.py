from jinja2 import Environment, FileSystemLoader


def render_template(template, folder='templates', static_url='/static/',
                    **kwargs):
    """

    :param template: name template
    :param folder: name of folder
    :param kwargs: parameters
    :return: rendered template
    :static_url: staticfiles
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    ren_template = env.get_template(template)

    return ren_template.render(**kwargs)
