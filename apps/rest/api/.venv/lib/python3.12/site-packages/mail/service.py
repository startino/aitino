"""\
Simple service which requires slightly more work to wrap the whole library
"""

import os
import logging

log = logging.getLogger(__name__)

from bn import AttributeDict, str_dict

from conversionkit import set_error
from conversionkit.exception import ConversionKitError

def exacltyOneFieldFrom(*fields):
    def exacltyOneFieldFrom_post_converter(conversion, state=None):
        found = []
        for k in conversion.children.keys():
            if k in fields:
                found.append(k)
        if len(found) == 2:
            set_error(
                conversion,
                'You should only specify %r or %r, not both'%(
                    found[0],
                    found[1],
                )
            )
        elif not found:
            set_error(
                conversion,
                'You must specify one of the fields %r'%(
                    fields,
                )
            )
    return exacltyOneFieldFrom_post_converter

def requireIfPresent(present, fields):
    """\
    Sets an overall error is the field ``present`` is present and any of the 
    fields in the list ``fields`` is not.
    """
    if not isinstance(fields, (list, tuple)):
        raise ConversionKitError(
            'The ``fields`` argument should be a list or a tuple, not '
            '%r' % type(fields)
        ) 
    def requireIfPresent_post_converter(conversion, state=None):
        if present in conversion.children.keys():
            for field in fields:
                if not field in conversion.children.keys():
                    set_error(
                        conversion,
                        'The field %r, required if %r is present, could not '
                        'be found'%(field, present)
                    )
                    return
    return requireIfPresent_post_converter

def mailService():

    #@staticmethod
    #def create(service):
    #    if not service.app.config.has_key(service.name):
    #        config = MailService.config(service)
    #    return MailService(config)

    def mailService_constructor(service, name, *k, **p):
        from mail.helper import send_smtp, send_sendmail, prepare, plain
        # Imports
        from configconvert import handle_option_error, handle_section_error
        from nestedrecord import decodeNestedRecord
        from conversionkit import chainConverters, chainPostConverters, Conversion
        from stringconvert import unicodeToInteger, unicodeToBoolean, unicodeToUnicode
        from stringconvert.email import listOfEmails
        from recordconvert import toRecord
        from configconvert import existingFile, existingDirectory

        # Config parsing
        if not service.app.option.has_key(name):
            raise handle_section_error(service, name, "'%s.sendmail' or '%s.smtp.host'"%(name, name))

        to_unicode = unicodeToUnicode()
        smtp_converter = chainPostConverters(
            toRecord(
                 missing_errors = dict(
                     host = "The required option '%s.smtp.host' is missing" % (name,),
                 ),
                 empty_errors = dict(
                     host="The option '%s.smtp.host' cannot be empty"%(name,),
                 ),
                 missing_defaults = dict(starttls=False),
                 converters = dict(
                     host = to_unicode,
                     username = to_unicode,
                     password = to_unicode,
                     port = unicodeToInteger(),
                     starttls = unicodeToBoolean(),
                     verbose = unicodeToBoolean(),
                 )
            ),
            requireIfPresent('username', ['password']),
        )
        mail_converter = chainConverters(
            decodeNestedRecord(depth=1),
            chainPostConverters(
                toRecord(
                    converters = dict(
                        sendmail = existingFile(),
                        smtp = smtp_converter,
                        debug_folder = existingDirectory(),
                        to_email_override = listOfEmails(split_name=False),
                    ),
                ),
                exacltyOneFieldFrom('sendmail', 'smtp'),
            )
        )
        conversion = Conversion(service.app.option[name]).perform(
            mail_converter
        )
        if not conversion.successful:
            handle_option_error(conversion, name)
        else:
            service.app.config[name] = conversion.result

        if service.app.config[name].get('debug_folder') and not \
           os.path.exists(service.app.config[name]['debug_folder']):
            os.mkdir(service.app.config[name]['debug_folder']) 

        def send(
            message, 
            to, 
            from_email, 
            from_name, 
            subject=None,
            type='plain',
            charset=None,
        ):
            if service.app.config[name].get('to_email_override'):
                log.warning(
                    'Replacing the email %s with %s', 
                    to, 
                    service.app.config[name].get('to_email_override'),
                )
                to = service.app.config[name].get('to_email_override')
            if to and isinstance(to, list) and isinstance(to[0], dict):
                to = ['%s <%s>'%(x.name, x.email) for x in to]
            subject = subject or service.app.config[name]['subject']
            message = prepare(
                plain(message, type=type, charset=charset),
                from_name = from_name,
                from_email = from_email,
                to=to, 
                subject=subject,
            )
            debug_folder = service.app.config[name].get('debug_folder')
            if debug_folder:
                log.warning(
                    'Writing message to the debug folder, not sending '
                    'it directly'
                )
                fp = open(
                    os.path.join(
                        debug_folder, 
                        '%s - %s.txt'%(subject, to) 
                    ),
                    'wb'
                )
                fp.write(str(message))
                fp.close()
            else:
                sendmail = service.app.config[name].get('sendmail')
                if sendmail:
                    return send_sendmail(
                        message, 
                        sendmail,
                    )
                smtp_args = service.app.config[name]['smtp']
                return send_smtp(message, **str_dict(smtp_args))

        def start(service):
            service[name] = AttributeDict(send=send)
        def leave(service, error=False):
            pass
        return AttributeDict(start=start, enter=start, leave=leave)
    return mailService_constructor

MailPipe = mailService()
