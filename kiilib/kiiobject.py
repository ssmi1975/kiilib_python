import kii

class KiiObject:
    def __init__(self, bucket, id, data):
        self.bucket = bucket
        self.id = id
        self.data = data

    def getPath(self):
        return '%s/objects/%s' % (self.bucket.getPath(), self.id)

    def __str__(self):
        return "KiiObject(%s) " % self.id + str(self.data)
        
class ObjectAPI:
    def __init__(self, context):
        self.context = context

    def create(self, bucket, data):
        url = '%s/apps/%s/%s/objects' % (self.context.url,
                                      self.context.app_id,
                                      bucket.getPath())
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(data)
        if code != 201:
            raise kii.CloudException(code, body)
        id = body['objectID']
        return KiiObject(bucket, id, data)
        
    def updateBody(self, obj, type, data, size):
        url = '%s/apps/%s/%s/body' % (self.context.url,
                                      self.context.app_id,
                                      obj.getPath())
        client = self.context.newClient()
        client.method = "PUT"
        client.url = url
        client.setContentType(type)
        client.setKiiHeaders(self.context, True)
        (code, body) = client.sendFile(data, size)
        if code == 200:
            return
        if code == 201:
            return
        raise kii.CloudException(code, body)

    def downloadBody(self, obj, outFile):
        url = '%s/apps/%s/%s/body' % (self.context.url,
                                      self.context.app_id,
                                      obj.getPath())
        client = self.context.newClient()
        client.method = "GET"
        client.url = url
        client.setKiiHeaders(self.context, True)
        (code, body) = client.sendForDownload(outFile)
        if code == 200:
            return
        raise kii.CloudException(code, body)
