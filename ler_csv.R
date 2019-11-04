library("XML")
library("openxlsx")
getwd()
setwd("C:/Users/cgt/Documents/carlos/SCRAP/scrap_detalhamento_servidor/")

dados <-  read.csv2("servidores.csv", header = FALSE, sep = ",", stringsAsFactors = FALSE)

db <- dados

nomes_coluna <- c("Detalhar", "Tipo", "CPF", "Nome_do_Servidor", "Orgao_Super_Serv_Lotacao",
                  "Orgao_Serv_Lotacao", "Orgao_Super_Serv_Exercicio", "Orgao_Serv_Exercicio",
                  "UORG_Serv_Lotacao", "UORG_Serv_Exercicio", "Matricula", "Tipo_de_vinculo",
                  "Cargo", "Atividade", "Funcao", "Licenca", "Quantidade")

names(db) <-  nomes_coluna

str(db)

#grava o arquivo 
write.xlsx(db, "Servidores_marinha.xlsx")

teste <- read.csv2("teste.csv", header = TRUE, sep = ",")
