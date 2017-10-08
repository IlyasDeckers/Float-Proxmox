#!/bin/python

import json
import simplejson
import logging

class Config():
  def __init__(self):
    self.config_file = '/etc/float-proxmox/config.json'

  def read(self):
    o = open(self.config_file)
    with o as json_data_file:
        data = json.load(json_data_file)
    return data
    o.close()

  def write(self, file):
    o = open(self.config_file, "w")
    o.write(
      simplejson.dumps(simplejson.loads(file), 
                       indent=4, 
                       sort_keys=True)
    )
    o.close()

  def update_hash(self, proxmox_token):
    file = self.read()
    file['proxmox']["auth_token"] = proxmox_token
    file = json.dumps(file)
    self.write(file)