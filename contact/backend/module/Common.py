#!/usr/bin/python
# coding:utf-8


import os
from Logger import Logger


def Timer(func):
    '''
    The function is a decorator,use it can tell you the runtime of a function.
    Example:
            @Timer
            def TestFunction(){}
    '''

    def call(*args, **kargs):
        import time
        common = Common(debug=True)
        start = time.time()
        result = func(*args, **kargs)
        end = time.time()
        common.msg("%s run time:%s" % (func.__name__, end - start))
        return result

    return call


class Common:
    def __init__(self, debug=False):
        import uuid
        self.logger = Logger().logger
        self.uuid = uuid
        self.debug = debug
        import struct
        self.struct = struct
        import socket
        self.socket = socket

    def msg(self, message):
        self.logger.debug(message)

    def message(self, message):
        self.logger.debug(message)

    def random_uuid(self):
        return str(self.uuid.uuid4())

    def email(self, from_address, to_addresses, subject, body, server='localhost', mimetext='plain',
              passwd=None, cc_addresses=None, attachments=None):
        if type(to_addresses) != list:
            to_addresses = [to_addresses]
        import smtplib
        import mimetypes
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email import encoders

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = ','.join(to_addresses)
        msg['Accept-Language'] = "zh-CN"
        msg['Accept-Charset'] = "ISO-8859-1,utf-8"
        msg.attach(MIMEText(body, mimetext, 'utf-8'))
        if cc_addresses:
            if type(cc_addresses) != list:
                cc_addresses = [cc_addresses]
            msg['Cc'] = ','.join(cc_addresses)
            to_addresses += cc_addresses
        if attachments:
            if type(attachments) != list:
                attachments = [attachments]
            for f in attachments:
                try:
                    ctype = mimetypes.guess_type(f)[0].split('/')[1]
                except:
                    ctype = 'octet-stream'
                with open(f, 'rb') as fp:
                    record = MIMEBase('application', ctype)
                    record.set_payload(fp.read())
                    encoders.encode_base64(record)
                    record.add_header('Content-Disposition',
                                      'attachment', filename=os.path.basename(f))
                msg.attach(record)
        s = smtplib.SMTP(server)
        if passwd:
            s.login(from_address, passwd)
        s.sendmail(from_address, to_addresses, msg.as_string())
        s.quit()

    def chat_message(self, to_user, message, typ='normal', from_user='publish', from_password='publish'):
        try:
            message = message.decode('utf-8')
        except:
            pass
        if from_user == 'publish':
            from_user = 'publish'
            from_password = 'publish'
        import xmpp
        jid = xmpp.protocol.JID("%s@chat.base-fx.com" % from_user)
        client = xmpp.Client(jid.getDomain(), debug=[])
        client.connect(('chat.base-fx.com', 5222), secure=0)
        client.auth(jid.getNode(), from_password)
        client.sendInitPresence()
        client.send(xmpp.protocol.Message("%s@chat.base-fx.com" %
                                          to_user, message, typ=typ))

    def ip_to_int(self, ip_string):
        '''
        Cover the address ip to the int ip.
        '''
        return self.struct.unpack('!l', self.socket.inet_aton(ip_string))[0]

    def int_to_ip(self, ip_int):
        '''
        Cover the int ip to the address ip.
        '''
        if ip_int < 0:
            ip_int = self.struct.unpack('I', self.struct.pack('i', ip_int))[0]
        return self.socket.inet_ntoa(self.struct.pack('I', self.socket.htonl(ip_int)))

    def get_files(self, file_path, filter_extension=True):
        '''
        Get files in the file_path.
        file_path--string The file's full path.
        filter_format--bool True:Get the file by extension;False:Just get all the files in the path.
        return--list The list contains all the files.
        '''
        import glob
        if not os.path.exists(file_path):
            return []
        mask = '%s/*' % os.path.dirname(file_path)
        if filter_extension:
            mask += '%s' % os.path.splitext(file_path)[1]
        return glob.glob(mask)

    def file_infos(self, file_path):
        '''
        Get the infomation of the file.
        file_path--string The file's full path.
        return--dictionary The infomation of the file.
        '''
        import magic
        magic_mime = magic.Magic(flags=magic.MAGIC_MIME_TYPE)
        magic_normal = magic.Magic()
        if not os.path.exists(file_path):
            return {}
        file_infos = {
            'name': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'format_details': magic_normal.id_filename(file_path).lower()
        }
        file_infos['format_type'], file_infos['format'] = magic_mime.id_filename(
            file_path).split('/')
        return file_infos

    # TODO THIS IS NOT A COMMON FUNCTION. PUT IT SOMEWHERE THAT MAKES SENSE
    def image_has_error(self, file_path):
        '''
        Check the image ,if the image has some errors,return True.
        file_path--string The file's full path.
        return--bool True/False
        '''
        from PIL import Image
        import OpenEXR
        if not os.path.exists(file_path):
            return True
        files = self.file_infos(file_path)
        if files['size'] == 0:
            return True
        if files['name'].endswith('.exr'):
            if 'image' not in files['format_details']:
                return True
        else:
            if files['format_type'] != 'image':
                return True
        if files['name'].endswith('.exr') or 'openexr' in files['format_details']:
            # [TIP]--Check the file if it's exr file--
            if not self.OpenEXR.isOpenExrFile(file_path):
                return True
            else:
                # [TIP]--Sometimes file is right,but file is not complete,so check the file if some data is missing--
                try:
                    f = self.OpenEXR.InputFile(file_path)
                except IOError:
                    return True
                if not f.isComplete():
                    return True
        else:
            try:
                image = self.Image.open(file_path)
                image.verify()
            except:
                return True
        return False

    def create_file(self, filePath, fileName):
        '''
        Create a config file in the a path.
        filePath--string, the directory path of the file.
        fileName--string, the name of the file.
        retur--bool, True: success;False:Fail.
        '''
        fullPath = "%s%s" % (filePath, fileName)
        dirs = filePath.split(r'/')
        curentDir = ""
        for dir in dirs:
            curentDir += "/%s/" % dir
            if not os.path.isdir(curentDir):
                os.mkdir(curentDir)
                # if not os.path.isdir(filePath):
                # os.mkdir(filePath)
        if not os.path.isfile(fullPath):
            open(fullPath, 'w')
        return os.path.isfile(fullPath)
