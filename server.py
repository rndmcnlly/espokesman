#!/usr/bin/python

import sys
from twisted.web import server, resource
from twisted.internet import reactor, protocol

class SpeechProtocol(protocol.ProcessProtocol):
  def __init__(self, text, output):
    self.text = text
    self.output = output

  def connectionMade(self):
    self.transport.write(self.text)
    self.transport.closeStdin()

  def outReceived(self, data):
    self.output.write(data)
  
  def processExited(self, status):
    self.output.finish()

class SpeechRenderer(resource.Resource):
  isLeaf = True
  def render(self, request):
    text = request.args['text'][0]
    request.setResponseCode(200)
    request.setHeader('Content-type', 'audio/mpeg')
    reactor.spawnProcess(
        SpeechProtocol(text,request),
        "./render_speech_to_mp3.sh")
    return server.NOT_DONE_YET

if __name__ == "__main__":
  root = resource.Resource()
  root.putChild("speech", SpeechRenderer())
  site = server.Site(root)
  reactor.listenTCP(8999, site)
  reactor.run()
