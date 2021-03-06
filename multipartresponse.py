#!/usr/bin/python

from bottle import route, run, request, response, install
import uuid
import glob
import os
import catio

@route("/")
def returnmultipart():
    boundary='----multipart-boundary-%s----' % (uuid.uuid1(),)
    response.content_type = 'multipart/mixed; boundary=%s' % (boundary,)
    s = catio.CatIO()

    for fn in glob.glob("*.dcm"):
        s += "\r\n" + boundary + "\r\n"
        s += 'Content-Disposition: attachment; filename="%s";\r\n' % (fn,)
        s += 'Content-Type: application/dicom;\r\n'
        s += 'Content-Length: %i\r\n' % (os.stat(fn).st_size,)
        s += '\r\n'
        s += file(fn)

    s += '\r\n' + boundary + '\r\n'

    s.seek(0,2)
    response.content_length = s.tell()
    s.seek(0)

    return s
    

run(host='localhost', port=5000)
