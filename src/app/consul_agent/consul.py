#!/bin/python

import consul

class Consul():
  def __init__(self, address="127.0.0.1", port="8500"):
    self.port = port
    self.address = address
    self.c = self.connect()

  def connect(self):
    return consul.Consul(self.address, self.port)

  def test_connection(self):
    return self.c.agent.self()

  def get_service(self, service):
    return self.c.catalog.service(service)

  def deregister_service(self,service_id):
    return self.c.agent.service.deregister(service_id)

  def register_service(self, service_name, vmid, port, address, tags):
    # register(name, service_id=None, address=None, port=None, tags=None, check=None, token=None, script=None, interval=None, ttl=None, http=None, timeout=None, enable_tag_override=False)
    self.c.agent.service.register(service_name, 
                              service_id=vmid, 
                              port=port, 
                              address=address,
                              tags=[tags])