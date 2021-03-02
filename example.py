from api import Facebook
import json

with open('system_user.json', 'r') as file:
    system_user = json.load(file)
bot = Facebook(version='v10.0', system_user=system_user)

with open('facebook_ids.json','r') as file:
    app_credentials = json.load(file)
bot.set_appId_pageId(**app_credentials)

image_locs = ['temp.JPG', 'logo.png']
media = []
for loc in image_locs:
    media.append(bot.upload_image(loc))

bot.page_post('First post from api', media)