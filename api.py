import requests
import json
import os.path

class Facebook(object):
    def __init__(self, version, system_user):
        """Generate Facebook api object

        Args:
            version (str): api version you wat to use (latest- 'v10.0')
            system_user (dict): dictionary containing system_user id and access_token
        """
        self.version = version
        self.BASE_URL = 'https://graph.facebook.com/'+self.version+'/'
        
        self.system_user = system_user
        self.generate_access_token(system_user['access_token'])
        self.app_set = False
        
    def set_appId_pageId(self, appId, appSecret, pageId):
        """Set facebook developer app and facebook page 

        Args:
            appId (str): appId (from developer.facebook.com)
            appSecret (str): addSecret (from developer.facebook.com)
            pageId (str): facebook page id (from facebook page's info section)
        """
        self.appId = appId
        self.appSecret = appSecret
        self.pageId = pageId
        self.app_set = True
        
    def generate_access_token(self, system_user_token):
        """It will generate access token for passed system user if no token is present

        Args:
            system_user_token (str): token of system user (generated from business.facebook.com)
        """
        if os.path.isfile('access_token.json'):
            with open('access_token.json', 'r') as file:
                credentials = json.load(file)
        else:
            response = requests.get(self.BASE_URL + 'me/accounts?access_token=' + system_user_token)
            credentials = response.json()
            with open('access_token.json', 'w') as file:
                json.dump(credentials, file, indent=4)
            
        self.token = {}
        self.token['access_token'] = credentials['data'][0]['access_token']
    
    # def get_post(self, post_id):
    #     response = requests.get(self.BASE_URL+post_id, self.token)
        
    def upload_image(self, image_loc):
        """upload local image to facebook server (unpublished). images will be deleted after 24 hrs. 

        Args:
            image_loc (str): path of image to be uploaded

        Returns:
            dict: dictionary containing id of uploaded media
        """
        image = {
            # 'content-type': "multipart/form-data",
            'source':open(image_loc, "rb")
        }
        data = {'published':False}
        data.update(self.token)
        response = requests.post(self.BASE_URL+self.pageId+'/photos', files=image, data=data)
        media = {}
        media['media_fbid'] = response.json().pop('id')
        return media
    
    def page_post(self, message, attached_media=None):
        """post message (with unpublished images) in page feed

        Args:
            message (str): message to be posted
            attached_media (list, optional): list of media dictionaries containing media_id. Defaults to None.
        """
        data = {
            'message': message,
            'published':True
        }
        if attached_media is not None:
            data.update({ 'attached_media': json.dumps(attached_media) })
        data.update(self.token)
        
        response = requests.post(self.BASE_URL+self.pageId+'/feed', data=data)
        return response.json()