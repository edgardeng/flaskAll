#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import login_manager
from .user import User
from .permission import Permission
from .comment import Comment
from .article import Article
from .role import Role

# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
