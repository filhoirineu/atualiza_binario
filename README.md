# ATUALIZA BINÁRIO

Toda vez que precisamos atualizar o binário do protheus é sempre a mesma coisa:

- baixa o binário atualizado do portal
- substitui o binário atualizado na pasta do balance/servers
- renomeia o appserver.exe de acordo com a necessidade
- copia dll extras
- meia lua para frente e soco
- repete isso para X (tendendo ao infinito) servers

Brincadeiras a parte,
Já temos o UPDDISTR para se preocupar, para que se preocupar com o isso.

Com esse objetivo, foi desenvolvido essa ferramenta


# ATUALIZA_BINARIO.INI

Deverá ser configurado o arquivo INI para processamento:

atualiza_binario: indica quais a sessoes do arquivo serão executadas
binario_atualizado: determina onde está o binário atualizado (que será replicado)

# SESSÕES

pasta_binario: pasta de onde se encontra o binário que será atualizado
appserver_exe: nome do appserver.exe que será tratado
appserver_ini: nome do appserver.ini que será tratado
ambiente: ambiente que sofrerá alterações (funcao ajusta_arquivo_ini)

Exemplo:


```ini
[_balance]
pasta_binario = D:\area_teste\Protheus_Bin\bin\_balance
appserver_exe = appserver_balance.exe
appserver_ini = appserver_balance.ini
ambiente = PARANOA
```

# ajusta_arquivo_ini

- Ajusta o INACTIVETIMEOUT do ambiente para 1800
- Ajusta o consolemaxsize para 25000000
- Ajusta o maxstringsize para 15