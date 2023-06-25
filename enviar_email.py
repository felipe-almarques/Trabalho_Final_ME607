import smtplib

# Para poder enviar o email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Para poder anexar no email
from email.mime.base import MIMEBase
from email import encoders

# Startar o servidor SMTP
host = 'smtp.gmail.com'
port = '587'
login = 'gruposeriestemporais@gmail.com'
senha = 'fdznkggxrdhuxsdc'

server = smtplib.SMTP(host, port)
server.ehlo()
server.starttls()
server.login(login, senha)

## Lembra de deixar o google menos seguro:
# Manager your Google Account >> Segurança >> Acesso a App menos seguros >> Ativar Acesso

# Construir o email tipo MIME

corpo = "Salve meu parcero"

email_msg = MIMEMultipart()
email_msg['From'] = login
email_msg['To'] = "f236106@dac.unicamp.br"
email_msg['Subject'] = "Meu e-mail enviado automaticamente"
email_msg.attach(MIMEText(corpo, 'html')) # pode ser 'plain' também

# Anexar arquivos
# Abrimos o arquivo em modo leitura e binary  
cam_arquivo = "data/2023-06-25_valor_predito.csv"
attachment = open(cam_arquivo, 'rb') # read binary

# Lemos o arquivo em modo binario e jogamos codificado em modo 64 (que é oq o email precisa)
att = MIMEBase('application', 'octet-stream')
att.set_payload(attachment.read())
encoders.encode_base64(att)

# Adicionamos o cabeçalho no tipo anexo de email
att.add_header('Content-Disposition', 'attachment; filename= nome_do_arquivo')
# Fechamos o arquivo
attachment.close()
# Colocamos o anexo no corpo do email
email_msg.attach(att)

# Enviar email tipo MIME no servidor SMTP
server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

server.quit()

print("O email foi enviado")
