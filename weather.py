from plugins import PluginManager


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     sender = message.author
#     content = message.content

class WeatherPlugin(PluginManager):

    def __init__(self, bot_obj):
        super(WeatherPlugin, self).__init__(bot_obj)
        self.register_plugin('Weather')

def run_weather():
    weather = WeatherPlugin()

run_weather()
