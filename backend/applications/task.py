# there are 2 scheduled task , 1 - monthly report and 2 - daily reminder
from .worker import celery
from .model import Users,Orders
from celery.schedules import crontab
from jinja2 import Template
# We will need smtplib to connect to our smtp email server
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import os

def send_mail(email,subject,email_content,attachment=None):
    # Define email server and credentials
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@gmail.com"
    sender_password = ""

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    # Attach the HTML content to the email
    msg.attach(MIMEText(email_content, "html"))

    # To export the csv to mail
    if attachment:
        with open(attachment,"rb") as attachment_content:
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % {os.path.basename(attachment)})
        part.add_header('Content-Disposition', f'attachment; filename= "{os.path.basename(attachment)}"')
            
        # Attach the part to the email
        msg.attach(part)

    # Set up email server
    server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail Sent")

def get_html_report(username,data):
    # Read the Jinja2 email template
    with open("report.html", "r") as file:
        jinja_template = Template(file.read())
        html_report=jinja_template.render(username=username,data=data)
        return html_report


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #calls test('hello') every 10 sec.
    sender.add_periodic_task(10.0, monthly_report.s(), name='report at every 10sec for test')

    # It uses the same signature of prev task, an explicit name is defined to avoid this task replacing the prev one defined.
    sender.add_periodic_task(10.0,daily_reminder.s(),name='daily reminder at every 10sec for test')

    #Executes every monday morning at 7:30 am.
    sender.add_periodic_task(
        crontab(hour=7, minute=30),
        daily_reminder.s(),
        name='daily_reminder at every 7:30 am'
    )

    #execute on the first day of every month
    sender.add_periodic_task(
        crontab(day_of_month='1',month_of_year='*'),
        daily_reminder.s(),
        name='montly_report at list of every month'
    )

@celery.task
def test(arg):
    print(arg)

@celery.task
def daily_reminder():
    customers=Users.query.filter_by(role="customer").all()
    for customer in customers:
        msg=f'<h1>Hi {customer.name}! Please visit grocerystore </h1>'
        send_mail(email=customer.email_id,email_content=msg,subject="Daily Reminder")
    print('Reminder Done')
        
@celery.task
def monthly_report():
    customers=Users.query.filter_by(role="customer").all()
    for customer in customers:
        orders=Orders.query.filter_by(user_id=customer.id).all()
        order_details=[]
        for order in orders:
            temp_dict={}
            temp_dict["product_id"] = order.product_id
            temp_dict["quantity"] = order.quantity
            temp_dict["date_of_purchase"] = order.date_of_purchase
            temp_dict["product_name"] = order.product.name
            temp_dict["product_price"] = order.product.price
            temp_dict["product_unit"] = order.product.unit
            order_details.append(temp_dict)

        html_report=get_html_report(username=customer.name,data=order_details)
        send_mail(email=customer.email_id,email_content=html_report,subject="Monthly Report")
    print("Report Sent!")


@celery.task
def data_export(product_details, email): #product details should be list of dict
    with open('data_export.csv','w',newline='') as csvfile:
        fieldnames = ['name', 'price', 'description', 'unit', 'stock', 'sold']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(product_details)
    send_mail(email=email,email_content="Please find the exported data.",subject="Product Data Export",attachment="data_export.csv")
    return "Data Exported!!"





            # temp_order=[]
            # temp_order.append(order.product_id)
            # temp_order.append(order.quantity)
            # temp_order.append(order.date_of_purchase)
            # temp_order.append(order.product.name)
            # temp_order.append(order.product.price)
            # temp_order.append(order.product.unit)
            # order_details.append(temp_order)

# sender.add_periodic_task(
    #     crontab(hour=8, minute=0, day_of_week=1),  # Every Monday at 8 AM
    #     weekly_order_report.s(),
    #     name="Send weekly order report"
    # )

        #     temp_dict={}
        #     temp_dict["product_id"] = order.product_id
        #     temp_dict["quantity"] = order.quantity
        #     temp_dict["date_of_purchase"] = order.date_of_purchase
        #     temp_dict["product_name"] = order.product.name
        #     temp_dict["product_price"] = order.product.price
        #     temp_dict["product_unit"] = order.product.unit
        #     order_details.append(temp_dict)




# @celery.task
# def weekly_order_report():
#     customers = Users.query.options(joinedload(Users.orders)).filter_by(role="customer").all()

#     for customer in customers:
#         orders = Orders.query.filter_by(user_id=customer.id).all()

#         if orders:
#             # Render email template with customer order data
#             html_content = render_template("report.html", customer=customer, orders=orders)

#             # Send email
#             send_email(
#                 subject=f"Your Weekly Order Report - {customer.name}",
#                 recipient=customer.email_id,
#                 body="Please find your weekly order report attached.",
#                 html=html_content
#             )

#     print("Weekly order reports sent successfully!")


# # Function to send an email
# def send_email(subject, recipient, body, html):
#     msg = Message(
#         subject=subject,
#         recipients=[recipient],
#         body=body,
#         html=html,
#         sender="your-email@example.com"
#     )
#     mail.send(msg)


