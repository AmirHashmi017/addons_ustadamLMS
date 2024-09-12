# -*- coding: utf-8 -*-

from . import controllers
from . import models


def post_init_hook(env):
    env['forum.forum'].create_crowdfunding_forum()
