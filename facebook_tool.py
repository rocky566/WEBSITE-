import os
import time
import requests
from bs4 import BeautifulSoup as sop


class FacebookTool:
    def __init__(self, task_id, post_url, cookies, delay, comments_file):
        self.task_id = task_id
        self.post_url = post_url
        self.cookies = self._parse_cookies(cookies)
        self.delay = delay
        self.comments_file = comments_file

    def _parse_cookies(self, cookies_string):
        cookies = {}
        for cookie in cookies_string.split(";"):
            if "=" in cookie:
                key, value = cookie.split("=", 1)
                cookies[key.strip()] = value.strip()
        return cookies

    def run(self):
        try:
            with open(self.comments_file, 'r') as file:
                comments = file.readlines()
            for i, comment in enumerate(comments):
                self._post_comment(comment.strip())
                time.sleep(self.delay)
        except Exception as e:
            print(f"[ERROR] Task {self.task_id}: {e}")

    def _post_comment(self, comment):
        session = requests.Session()
        try:
            response = session.get(self.post_url, cookies=self.cookies)
            soup = sop(response.text, 'html.parser')
            comment_form = soup.find('form', {'method': 'post'})
            action_url = comment_form['action']
            payload = {input_tag['name']: input_tag.get('value', '') for input_tag in comment_form.find_all('input')}
            payload['comment_text'] = comment
            session.post(action_url, data=payload, cookies=self.cookies)
            print(f"[INFO] Task {self.task_id}: Posted comment '{comment}'")
        except Exception as e:
            print(f"[ERROR] Failed to post comment: {e}")
