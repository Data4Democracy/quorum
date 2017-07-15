import unittest

import sys
import os
sys.path.append(os.path.abspath(os.path.join('../')))
from fb_api_pages import format_post

class TestFB(unittest.TestCase):

    def setUp(self):
        pass

    def test_format_posts(self):

        post = {}
        post["id"] = "someID"
        post["created_time"] = "1/1/1900 11:00am"
        post["from"] = {"name": "DarthDippy"}

        post["message"] = "Dank Memes Very Where"
        post["link"] = "No Links"
        ret = format_post(post)


        self.assertEqual(ret["idstr"], "someID")
        self.assertEqual(ret["created_at"], "1/1/1900 11:00am")
        self.assertEqual(ret["author"], "DarthDippy")

        post["link"] = ['link1', 'link2', 'link3']

        ret = format_post(post)

        self.assertIn('link1', ret['urls'])
