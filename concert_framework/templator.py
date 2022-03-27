from jinja2 import Environment, FileSystemLoader

def render_template(template, folder='templates', static_url='/static/',
                    **kwargs):
    """

    :param template: name template
    :param folder: name of folder
    :param kwargs: parameters
    :return: rendered template
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    ren_template = env.get_template(template)

    # file_path = os.path.join(folder, template)

    # with open(file_path, encoding='utf-8') as f:
    #     template = Template(f.read())

    return ren_template.render(**kwargs)