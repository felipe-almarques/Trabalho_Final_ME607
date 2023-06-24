library(yfR)
library(rugarch)
library(tidyverse)

#### Criando a variável série ####
nome_acao <- "AAPL"   # Código no Yahoo Finance
data_ini  <- "2010-01-01" # Data de inicio
precos <- yf_get(tickers = nome_acao, first_date = data_ini)

serie <- precos$ret_adjusted_prices[-1]
serie <- serie - mean(serie)

#### Modelando a série ####

spec <- ugarchspec(mean.model = list(armaOrder = c(0, 0), include.mean = FALSE),
                   variance.model = list(model = 'sGARCH', garchOrder = c(1, 1)),
                   distribution = 'std')
fit <- ugarchfit(spec, serie, solver = 'hybrid')

ts.plot(serie)

#### Fazendo Previsão com o Modelo ####

previsao <- ugarchforecast(fit, n.ahead = 7)
fore_serie <- previsao@forecast$seriesFor
fore_sigma <- previsao@forecast$sigmaFor

df <- data.frame(serie=as.vector(fore_serie),
                 sigma=as.vector(fore_sigma))

write_csv(df, paste0('data/', Sys.Date(), '_valor_predito.csv'))
