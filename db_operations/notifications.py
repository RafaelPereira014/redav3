import logging
import smtplib
import os
import mysql.connector  # Import MySQL Connector Python module
from config import DB_CONFIG  # Import the database configuration
from flask import current_app, session, url_for
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email.mime.text import MIMEText
from db_operations import *

def connect_to_database():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def send_email(to_emails, subject, message):
    from_email = "noreply@azores.gov.pt"
    password = "JMLpUW7tsA9bgkoq"  # Use your actual password here
    smtp_server = "pegasus.azores.gov.pt"
    user = "s0204redaproj"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(user, password)
        for to_email in to_emails:
            msg['To'] = to_email
            server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_email_on_resource_create(resource_id, username, resource_link, recipient_emails):
    subject = f"Novo recurso criado #{resource_id}."
    message = f"""
    <p>Foi adicionado um novo recurso na plataforma REDA pelo utilizador {username}</p>
    <p>Pode visualizar os seus detalhes em {resource_link}</p>
    """
    send_email(recipient_emails, subject, message)

def send_email_on_resource_update(resource_id):
    to_email = "user@example.com"  # Fetch the user's email address from the database
    subject = "Recurso atualizado"
    message = f"""
    <p>Foi atualiado o recurso {{nomedorecurso}} na plataforma REDA pelo utilizador {{username}}</p>
    <p>Pode visualizar os seus detalhes em {{linkparaorecurso}}</p>
    """
    send_email(to_email, subject, message)
    
def send_email_on_script_received(script_id):
    to_email = "user@example.com"  # Fetch the user's email address from the database
    subject = "Proposta de operacionalização recebida."
    message = f"""
    <p>Foi introduzida uma nova proposta de operacionalização no recurso {{nomedorecurso}}.</p>
    <p>Pode visualizar os seus detalhes em {{linkparaorecurso}}.</p>
    """
    send_email(to_email, subject, message)

def send_email_on_script_approval(script_id):
    to_email = "user@example.com"  # Fetch the user's email address from the database
    subject = "Proposta de operacionalização aprovada."
    message = f"<p>A sua proposta de operacionalização para o recurso {{nomedorecurso}} foi aprovada.</p>"
    send_email(to_email, subject, message)

def send_email_on_comment_received(comment_id):
    to_email = "user@example.com"  # Fetch the user's email address from the database
    subject = "Novo comentário recebido."
    message = f"""
    <p>Foi recebido um novo comentário no recurso {{nomedorecurso}}.</p>
    <p>Pode visualizar os seus detalhes em {{linkparaorecurso}}.</p>
    """
    send_email(to_email, subject, message)

def send_email_on_contact(contact_id):
    to_email = "user@example.com"  # Fetch the user's email address from the database
    subject = "Nova mensagem recebida."
    message = f"<p>Recebeu a seguinte mensagem acerca do recurso {{nomedorecurso}} : {{mensagem}}.</p>"
    send_email(to_email, subject, message)

