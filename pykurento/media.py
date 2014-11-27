import logging

logger = logging.getLogger(__name__)

# This is the object graph as described at http://www.kurento.org/docs/5.0.3/mastering/kurento_API.html
# We dont mimic it precisely yet as its still being built out, not all abstractions are necessary
#                   MediaObject
# Hub               MediaElement                MediaPipeline
#          HubPort    Endpoint    Filter
#           InputEndpoint OutputEndpoint


class MediaObject(object):
  def __init__(self, parent, **args):
    logger.debug("Creating new %s", self.__class__.__name__)
    self.parent = parent
    self.options = args
    self.id = self.get_transport().create(self.__class__.__name__, **args)

  def get_transport(self):
    return self.parent.get_transport()

  def get_pipeline(self):
    return self.parent.get_pipeline()

  def invoke(self, method, **args):
    return self.get_transport().invoke(self.id, method, **args)

  def subscribe(self, event, fn):
    def _callback(value):
      fn(value, self)
    return self.get_transport().subscribe(self.id, event, _callback)

  def release(self):
    return self.get_transport().release(self.id)


class MediaPipeline(MediaObject):
  def get_pipeline(self):
    return self


class MediaElement(MediaObject):
  def __init__(self, parent, **args):
    args["mediaPipeline"] = parent.get_pipeline().id
    super(MediaElement, self).__init__(parent, **args)

  def connect(self, sink):
    return self.invoke("connect", sink=sink.id)


# ENDPOINTS

class HttpGetEndpoint(MediaElement):
  pass


class HttpPostEndpoint(MediaElement):
  pass


class PlayerEndpoint(MediaElement):
  pass


class RecorderEndpoint(MediaElement):
  pass


class RtpEndpoint(MediaElement):
  pass

  
class WebRtcEndpoint(MediaElement):
  def generateOffer(self):
    return self.invoke("generateOffer")

  def processOffer(self, offer):
    return self.invoke("processOffer", offer=offer)

  def processAnswer(self, answer):
    return self.invoke("processAnswer", answer=answer)

  def getLocalSessionDescriptor(self):
    return self.invoke("getLocalSessionDescriptor")

  def getRemoteSessionDescriptor(self):
    return self.invoke("getRemoteSessionDescriptor")


# FILTERS

class GStreamerFilter(MediaElement):
  pass


class FaceOverlayFilter(MediaElement):
  pass


class ZBarFilter(MediaElement):
  def on_code_found_event(self, fn):
    return self.subscribe("CodeFoundEvent", fn)


# HUBS

class Composite(MediaElement):
  pass


class Dispatcher(MediaElement):
  pass


class DispatcherOneToMany(MediaElement):
  pass
























