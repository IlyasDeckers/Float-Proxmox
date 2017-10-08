#!/bin/python

import os
import requests
import logging
from app.config.config import Config
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class Proxmox():
  def __init__(self):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    self.nodes = ['prox1', 'prox2', 'prox3']
    self.httpheaders = {'Accept':'application/json','Content-Type':'application/x-www-form-urlencoded'}
    self.config = Config().read()['proxmox']
    self.cookies = {'PVEAuthCookie': self.config['auth_token']}

  def request(self, method, request, data={}):
    proxmox_url = 'https://' + self.config['host'] + ':' + self.config['port'] + '/api2/json'

    if method == 'POST':
      try:
        response = requests.post(proxmox_url + request, 
                             verify=False, 
                             cookies=self.cookies, 
                             headers=self.httpheaders, 
                             data=data)
      except (ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError) as e:
          logging.info(e) 

    elif method == 'GET':
      try:
        response = requests.get(proxmox_url + request, 
                                verify=False, 
                                cookies=self.cookies, 
                                headers=self.httpheaders)

      except (ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError) as e:
          logging.info(e)

    if response.status_code == 200:
      return response.json()

    if response.status_code == 401:
      logging.info('Requesting new auth token.')
      self.get_token()
      os.execl('/usr/local/bin/float-proxmox', '')

  def get_token(self):
    r = requests.post('https://prox1.phasehosting.io:8006/api2/json/access/ticket', verify=False, data = {
      'username':self.config['username'],
      'password':self.config['password'],
     })

    try:
      Config().update_hash(r.json()['data']['ticket'])
      logging.info('Writing auth token to /etc/float-proxmox/config.json.')
    except TypeError as e:
      logging.info('Auth credentials are not correct. Exiting...')
      sys.exit(0)

  def get(self, service):
    result = []
    for node in self.nodes:
      r = self.request('GET', '/nodes/' + node + '/' + service)

      for x in r['data']:
        x['node'] = node
        if self.is_valid_hostname(x['name'].encode("idna").decode().split(":")[0]):
          result.append(x)
          
    consul_data = []
    for x in result:
      prox_data = self.request('GET', '/nodes/' + x['node'] + '/' + service + '/' + x['vmid'] + '/config')['data']

      data = {}
      data[x['name']] = {
          'node': x['node'],
          'vmid': x['vmid'],
          'hostname': x['name'],
          'network': prox_data['net0'],
          'application': prox_data['ostype']
      }

      consul_data.append(data[x['name']])

    logging.info('Successfully obtained lxc information.')
    return consul_data

  def is_valid_hostname(self,hostname):
    if len(hostname) > 255:
        return False

    hostname = hostname.rstrip(".")
    split = hostname.split(".")
  
    return (0 <= 1 < len(split)) or (-len(split) <= 1 < 0)