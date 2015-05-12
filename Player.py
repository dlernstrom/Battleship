# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os
from importlib import import_module
from shutil import copyfile


class Player(object):
    def __init__(self, name):
        #print "%s Player created with name: %s" % (self.__class__, name)
        self.name = name


class Human(Player):
    """ Human player"""


class AI(Player):
    def __init__(self, path):
        super(AI, self).__init__(os.path.basename(path))
        self.copy_file(path)
        self.import_and_validate_player()

    def copy_file(self, path):
        digest = hashlib.md5()
        with open(path) as f:
            contents = f.read()
            digest.update(contents)
            new_name = 'AI_' + digest.hexdigest()
        ext = os.path.splitext(path)[1]
        running_path = os.path.join(os.path.dirname(__file__),
                                    'AI', '%s%s' % (new_name, ext))
        self.mod_name = 'AI.' + new_name
        copyfile(path, running_path)

    def import_and_validate_player(self):
        my_module = import_module(self.mod_name)

        if not hasattr(my_module, 'AIPlayer'):
            raise Exception("AIPlayer doesn't exist in %s" % self.name)
        self.my_cls = my_module.AIPlayer()
        mod_api = ['config_fleet', 'get_coords_for_shot']
        for method in mod_api:
            if not hasattr(self.my_cls, method):
                raise Exception("%s doesn't exist in AIPlayer" % method)

    def config_fleet(self, fleet):
        try:
            return self.my_cls.config_fleet(fleet)
        except Exception, data:
            raise

    def get_coords_for_shot(self, current_board_api):
        return self.my_cls.get_coords_for_shot(current_board_api)
