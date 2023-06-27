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

#### Fazendo Previsão com o Modelo ####
## Previsão da volatilidade
previsao <- ugarchforecast(fit, n.ahead = 1)
fore_sigma <- previsao@forecast$sigmaFor

## Previsão do VaR e ES
xf = function(x, mu_, sigma_, shape_) {
  x*ddist(distribution = "std", 
          y = x,
          mu = mu_, 
          sigma = sigma_, 
          skew = 0,
          shape = shape_)
}

alpha <- 0.025
var <- qdist(distribution = "std", alpha, mu = previsao@forecast[["seriesFor"]][1], sigma = sigma(previsao)[1], skew = 0, shape = coef(fit)["shape"])
ES = integrate(xf, 
                -Inf, 
                var, 
                mu_ = previsao@forecast[["seriesFor"]][1],
                sigma_ = sigma(previsao)[1],
                shape_ = coef(fit)["shape"])$value/alpha

#### Criando o .csv ####

df <- data.frame(volatilidade = as.vector(fore_sigma),
                 VaR = var, ES = ES)

write_csv(df, paste0('data/', Sys.Date(), '_valor_predito.csv'))
