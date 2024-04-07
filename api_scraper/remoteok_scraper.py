from email.utils import COMMASPACE, formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
import smtplib
from xlwt import Workbook
import xlwt
import requests
from hide import hide


BASE_URL = "https://remoteok.com/api/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}


def get_job_postings():
    response = requests.get(url=BASE_URL, headers=REQUEST_HEADER, timeout=10)
    return response.json()


def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())

    for i in range(len(headers)):
        job_sheet.write(0, i, headers[i])

    for i in range(len(data)):
        job = data[i]
        values = list(job.values())

        for x in range(len(values)):
            job_sheet.write(i + 1, x, values[x])

    wb.save('remote_jobs.xls')

    print(headers)


def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = COMMASPACE.join(send_to)
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject

    message.attach(MIMEText(text))

    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))

        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        message.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(send_from, hide.email_password)
    smtp.sendmail(send_from, send_to, message.as_string())
    smtp.close()


if __name__ == "__main__":
    # json = get_job_postings()[1:]
    # output_jobs_to_xls(json)
    send_email('samipythontest@gmail.com', ['samuelendale7373@gmail.com', 'samuel.endale@aait.edu.et'],
               'jobs posting', 'please find the list of jobs to this email', files=['remote_jobs.xls'])
