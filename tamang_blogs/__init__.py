
from . import controllers
from . import models


def post_init_hook(env):
    env['blog.blog'].create_crowdfunding_blog()
    # env['forum.forum'].create_crowdfunding_forum()
