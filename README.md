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

execbinarios: indica quais as sessões do arquivo serão executadas
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

# PROCESSO

- o que estiver na chave pasta_binario será renomeado para @backup (D:\area_teste\Protheus_Bin\bin\@backup_balance)
- será criado uma nova pasta baseado na anterior renomeada (D:\area_teste\Protheus_Bin\bin\_balance)
- será copiado o novo binário (binario_atualizado) para a nova pasta
- renomeado o arquivo appserver.exe para (appserver_exe)
- será copiado o arquivo .ini (appserver_ini) da pasta @backup para a nova pasta
- ajusta o ambiente de acordo com o ajusta_arquivo_ini