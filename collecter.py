#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
import time
import urllib2
from twython import Twython

IMAGES_DIR = './'

#4つの鍵を入力する(両サイドの''は残す)
# Consumer key
CK='ココに入力'
# Consumer secret
CS='ココに入力'
# Access token
ATK='ココに入力'
# Access token secret
ATS='ココに入力'

NUM_PAGES       = 5   
TWEET_PER_PAGE  = 200 
 
# 画像を保存するファイル名
SCREEN_NAMES = '''
your_name
'''
 
 
class TwitterImageDownloader(object):
    """Twitterから画像をダウンロードする"""
    def __init__(self):
        super(TwitterImageDownloader, self).__init__()
        self.twitter =Twython(app_key=CK, app_secret=CS, oauth_token=ATK, oauth_token_secret=ATS)
 
    def read_ids(self):
        ids_all = [line.replace('@', '') for line in SCREEN_NAMES.splitlines() if line]
        ids = sorted(list(set(ids_all)))
        return ids
     
    def get_timeline(self, screen_name):
        max_id = ''
        url_list = []
        for i in xrange(NUM_PAGES):
            try:
                print 'getting timeline : @', screen_name, (i+1), 'page'
                #tw_result = (self.twitter.get_user_timeline(screen_name=screen_name, count=TWEET_PER_PAGE, max_id=max_id) if max_id else self.twitter.get_user_timeline(screen_name=screen_name, count=TWEET_PER_PAGE))
                tw_result = (self.twitter.get_home_timeline(count=TWEET_PER_PAGE, max_id=max_id) if max_id else self.twitter.get_home_timeline(count=TWEET_PER_PAGE))
                time.sleep(5)
            except Exception as e:
                print "timeline get error ", e
                break
            else:
                for result in tw_result:
                    if 'media' in result['entities']:
                        media = result['extended_entities']['media']
                        for url in media:
                            url_list.append(url['media_url'])
                    max_id = result['id']
            if len(tw_result) < TWEET_PER_PAGE:
                break
        return url_list
 
    def create_folder(self, save_dir):
        try:
            os.mkdir(save_dir)
        except Exception as e:
            print 'cannot make dir', e
        file_list = os.listdir(save_dir)
        return file_list
 
    def get_file(self, url, file_list, save_dir):
        file_name = url[url.rfind('/')+1:]
        url_large = '%s:large'%(url)
        if not file_name in file_list:
            save_path = os.path.join(save_dir, file_name)
            try:
                print "download", url_large
                url_req = urllib2.urlopen(url_large)
            except Exception as e:
                print "url open error", url_large, e
            else:
                print "saving", save_path
                img_read = url_req.read()
                img = open(save_path, 'wb')
                img.write(img_read)
                img.close()
                time.sleep(1)
        else:
            print "file already exists", file_name
 
    def download(self):
        screen_name_list = self.read_ids()
        num_users = len(screen_name_list)
        for i, screen_name in enumerate(screen_name_list):
            save_dir  = os.path.join(IMAGES_DIR, screen_name)
            file_list = self.create_folder(save_dir)
 
            url_list = self.get_timeline(screen_name)
            num_urls = len(url_list)
            for j, url in enumerate(url_list):
                self.get_file(url, file_list, save_dir)
                print "%d / %d users, %d / %d pictures"%((i+1), num_users, (j+1), num_urls)
 
def main():
    for i in range(60*60/(5*60)): # 計1時間回す
        tw = TwitterImageDownloader()
        tw.download()
        time.sleep(5*60) # 5分休む
 
if __name__ == '__main__':
    main()
    