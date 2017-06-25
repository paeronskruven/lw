import os
import configparser
import logging
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.lw/lw.conf'))

logger = logging.getLogger('LW')


def _send_email(new_items):
    logger.info('Preparing email')

    server = smtplib.SMTP(
        config.get('smtp', 'host'),
        config.get('smtp', 'port')
    )

    try:
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()

        server.login(
            config.get('smtp', 'user'),
            config.get('smtp', 'pass')
        )

        from_address = config.get('smtp', 'from')
        to_address = config.get('smtp', 'to')

        msg = MIMEMultipart('alternative')
        msg.set_unixfrom('ListingsWatch')
        msg['To'] = email.utils.formataddr((to_address, to_address))
        msg['From'] = email.utils.formataddr(('ListingsWatch', from_address))
        msg['Subject'] = 'ListingsWatch update'

        body = ['<h2>ListingsWatch</h2>']
        for key, items in new_items.items():
            body.append('<h4>{0}</h4><ul>'.format(key))
            for item in items:
                body.append(
                    '<li><a href="{0}">{1}</a> {2}</li>'.format(item.url, item.title, item.price)
                )
            body.append('</ul>')

        msg.attach(MIMEText(''.join(body), 'html'))

        server.sendmail(
            from_address,
            [to_address],
            msg.as_string()
        )

        logger.info('Email sent')

    except Exception as ex:
        logger.error(ex)
    finally:
        server.close()


def notify(items):
    logger.info('Notifying of new items')

    if config.getboolean('notifications', 'email'):
        _send_email(items)
