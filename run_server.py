from settings.environment    import app, RUN_SETTING
from settings.authentication import auth_view


app.add_url_rule('/auth/', view_func=auth_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(**RUN_SETTING)