import sublime, sublime_plugin
import urllib, urllib2
import threading

class RaspGpioCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get the server address
        first_line = self.view.substr(self.view.line(0))
        address = first_line.split('###!@address ')[1]

        # get the file content
        file_content = self.view.substr(sublime.Region(0, self.view.size()))

        # send the script to the server
        sendFileRequest = RaspGpioSendFile(address, file_content)
        sendFileRequest.start()
        sublime.status_message("RaspGpio: Sending file...")

class RaspGpioSendFile(threading.Thread):
    def __init__(self, address, file_content):
        self.address = address
        self.file_content = file_content

        threading.Thread.__init__(self)

    def run(self):
        try:
            print "Thread is running..."
            # pack data
            data = {'file_content': self.file_content}
            # set url
            request = urllib2.Request(self.address)
            # set 'Content-Type' to 'multipart/data' to send files
            # request.add_header("Content-Type", "multipart/data")
            # add file content (add_data will change the HTTP method to POST)
            request.add_data(urllib.urlencode(data))
            # send the request
            http_file = urllib2.urlopen(request)
            print "Request sent..."
            # get back the response
            self.result = http_file.read()
            print "Request done. Code status:", http_file.getcode()
            print self.result
            return

        except (urllib2.HTTPError) as (e):
            err = '%s: HTTP error %s' % (__name__, str(e.code))
        except (urllib2.URLError) as (e):
            err = '%s: URL error %s' % (__name__, str(e.reason))

        sublime.error_message(err)
        self.result = False
        print "Thread stopped."


