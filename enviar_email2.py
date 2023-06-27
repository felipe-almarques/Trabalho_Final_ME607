import smtplib
import pandas
import datetime

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

#cam_arquivo = "C:\\Users\\Família\\Desktop\\Arquivos\\Unicamp\\ME607\\Trabalho Final\\email\\Arquivo_teste.csv"
### Trabalhando na base de dados

hoje = datetime.date.today()
ontem = hoje - datetime.timedelta(1)

cam_arquivo_antigo = "data/" + str(ontem) + "_valor_predito.csv"
cam_arquivo_novo = "data/" + str(hoje) + "_valor_predito.csv"

df1 = pandas.read_csv(cam_arquivo_antigo)
df2 = pandas.read_csv(cam_arquivo_novo)
print("Baixou os df corretamente")

df = df1.append(df2, ignore_index=True)
print("criou o novo df")

df.to_csv(cam_arquivo_novo)
print("Escreveu o csv")

vol = df["volatilidade"][-1]
var = df["VaR"][-1]
es = df["ES"][-1]

corpo = f"Ao modelar a série de retorno das ações da Apple, o modelo escolhido GARCH(1,1) realizou previsões um passo a frente para algumas medidas importantes.\nDentre tais medidas, nosso modelo previu um valor de volatilidade igual a {vol}, valor de risco de {var} e perda prevista de {es}. O resultado fora apresentado no arquivo csv em anexa."

server = smtplib.SMTP(host, port)
server.ehlo()
server.starttls()
server.login(login, senha)

## Lembra de deixar o google menos seguro:
# Manager your Google Account >> Segurança >> Acesso a App menos seguros >> Ativar Acesso

# Construir o email tipo MIME

email_msg = MIMEMultipart()
email_msg['From'] = login
email_msg['To'] = "f236106@dac.unicamp.br"
email_msg['Subject'] = "Meu e-mail enviado automaticamente"
email_msg.attach(MIMEText(corpo, 'html')) # pode ser 'plain' também

# Anexar arquivos
# Abrimos o arquivo em modo leitura e binary  
attachment = open(cam_arquivo, 'rb') # read binary

# Lemos o arquivo em modo binario e jogamos codificado em modo 64 (que é oq o email precisa)
att = MIMEBase('application', 'octet-stream')
att.set_payload(attachment.read())
encoders.encode_base64(att)

# Adicionamos o cabeçalho no tipo anexo de email
att.add_header('Content-Disposition', 'attachment; filename= Previsao.csv')
# Fechamos o arquivo
attachment.close()
# Colocamos o anexo no corpo do email
email_msg.attach(att)

# Enviar email tipo MIME no servidor SMTP
server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

server.quit()
