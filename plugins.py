
class Plugins(object):

    def __init__(self):
        print(dir())


class PluginManager(Plugins):

    def __init__(self, bot):
        print(dir(bot))
        self.installed_plugins = []
        self.enabled_plugins = []

    def load_plugins(self):
        from weather import WeatherPlugin

    def register_plugin(self, plugin_data):
        self.installed_plugins += plugin_data
