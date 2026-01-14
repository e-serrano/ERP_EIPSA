import smtplib, base64, os
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from PIL import Image
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from datetime import date
from config.config import config, get_path
from config.config_keys import SMTP_SERVER, SMTP_PORT
from utils.Database_Manager import Database_Connection
from utils.Helpers import decrypt_password
from utils.Show_Message import MessageHelper

class BaseEmail:
    def __init__(self, smtp_username, list_emails):
        self.SMTP_SERVER = SMTP_SERVER
        self.SMTP_PORT = SMTP_PORT
        self.smtp_username = smtp_username

        self._parse_emails(list_emails)

        commands_usermail = ("""
                            SELECT "password"
                            FROM users_data.commercial_data
                            WHERE "email" = %s
                            """)

        original_password = None
        try:
            with Database_Connection(config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(commands_usermail, (self.smtp_username,))
                    results = cur.fetchall()
                    password = results[0][0]
                    original_password = decrypt_password(password)

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

        self.smtp_password = original_password

    def _parse_emails(self, list_emails: str):
        emails = list_emails.split("copia:")
        if len(emails) == 2:
            self.to_email = emails[0].strip()
            self.cc_email = emails[1].strip()
        else:
            self.to_email = list_emails.strip()
            self.cc_email = None

    def _load_image_base64(self, path):
        with open(path, 'rb') as f:
            image = Image.open(f)
            image.thumbnail((250, image.height))
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def send(self, subject, html_content):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = self.to_email
        if self.cc_email:
            msg['Cc'] = self.cc_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            recipients = self.to_email.split(',')

            if self.cc_email:
                recipients.extend(self.cc_email.split(','))

            server.sendmail(self.smtp_username, recipients, msg.as_string())

class EmailOffer(BaseEmail):
    def __init__(self, smtp_username, list_emails, num_offer, num_ref, pres_date):
        super().__init__(smtp_username, list_emails)
        self.num_offer = num_offer
        self.num_ref = num_ref
        self.pres_date = date.fromisoformat(str(pres_date))
        template_dir = str(get_path("Resources", "Email Templates"))
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_email(self, template_name):
        # Date data
        days_presentation = (date.today() - self.pres_date).days
        day, month, year = self.pres_date.strftime("%d-%m-%Y").split('-')
        months_english = ['January','February','March','April','May','June','July','August','September','October','November','December']
        months_spanish = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']

        # Set context
        context = ({
            'subject': f"Update status offer {self.num_ref} // {self.num_offer}",
            'num_ref': self.num_ref,
            'days_presentation': days_presentation,
            'day': int(day),
            'month_english': months_english[int(month)-1],
            'month_spanish': months_spanish[int(month)-1],
            'year': int(year)
        })

        # Load logo
        context['image_base64'] = self._load_image_base64(str(get_path("Resources", "Iconos", "Logo_email.png")))

        # Render template
        template = self.env.get_template(template_name)
        html_content = template.render(context)

        # Using method of parent class
        subject = context.get('subject', f"Update status offer {self.num_ref} // {self.num_offer}")
        self.send(subject, html_content)
