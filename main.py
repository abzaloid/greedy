# coding=utf-8

import os
import sys
import webapp2
import jinja2

import database
import search
import controllers
import admin
import cart
import calculate

import models

import user_controllers

from handler import Handler
from Forum import *


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

### Configuration ###
config = {}
config = {
      'webapp2_extras.auth': {
            'user_model': 'models.User',
            'user_attributes': ['name']
            },
      'webapp2_extras.sessions': {
            'secret_key': 'my secret key which you dont know'
      }
}


class ProfileHandler(Handler):
    def get(self):
        viewer = self.user_model
        self.render_google('profile.html',{'user':viewer})


app = webapp2.WSGIApplication([('/', controllers.MainPage),
                               webapp2.Route('/logout', user_controllers.LogoutHandler, name='logout'),
                               webapp2.Route('/login', user_controllers.LoginHandler, name='login'), 
                               ('/signup', user_controllers.SignupHandler),
                               ('/password', user_controllers.SetPasswordHandler),
                               webapp2.Route('/forgot', user_controllers.ForgotPasswordHandler, name='forgot'),
                               webapp2.Route('/authenticated', user_controllers.AuthenticatedHandler, name='authenticated'),
                               webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>', user_controllers.VerificationHandler, name='verification'),
                               ('/cart/add', cart.AddToCartHandler),
                               ('/about', controllers.AboutHandler),
                               ('/change_profile', user_controllers.ChangeProfile),
                               ('/done', cart.DoneHandler),
                               ('/mainpage', controllers.MainPage),
                               ('/forum/(\w+)', ForumHandler),
                               ('/forum/(\w+)/(\w+)', ForumCommentHandler),
                               ('/vote', VoteHandler),
                               ('/profile', ProfileHandler),
                               ('/forum', ForumViewer),
                               ('/forum/', ForumViewer),
                               ('/cart', cart.CartHandler),
                               ('/checkout', cart.CheckoutHandler),
                               ('/sendmail', admin.EmailHandler),
                               ('/submit', SubmissionHandler),
                               ('/listorders', cart.ListOrdersHandler),
                               ('/secure', controllers.SecureHandler),
                               ('/update_database', database.UpdateDatabase),
                               ('/update_forum', database.UpdateForum),
                               ('/search', search.SearchItem),
                               ('/lookfor', search.LookForItem),
                               ('/shopping_list', calculate.ShowShoppingList),
                               ('/additem', calculate.addItemToCart),
                               ('/delitem', calculate.delItemFromCart),
                               ('/all-subcategory/(\d+)', controllers.SubCategoryAJAX),
                               ('/all-subcategory-except/(\d+)', controllers.SubCategoryAJAXExcept),
                               ('/empty_cart', cart.EmptyCart),
                               ('/deleteitem', database.DeleteItemDatabase),
                               ('/category/(\d+)', controllers.ShowCategoryHandler),
                               ('/category/(\d+)/(\d+)', controllers.ShowCategoryWithPaginationHandler),
                               ('/subcategory/(\d+)/(\d+)', controllers.ShowSubCategoryHandler),
                               ('/subcategory/(\d+)/(\d+)/(\d+)', controllers.ShowSubCategoryWithPaginationHandler)], 
                               config=config, debug=True)
