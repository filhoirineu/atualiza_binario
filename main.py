import os
from time import sleep
from configparser import ConfigParser
from traceback import format_exc
from datetime import datetime

def renomeia_pasta(antes, depois):
    os.rename(antes, depois)

def cria_pasta(nova_pasta):
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)

def copia_novo_binario(binario_atualizado,pasta_binario):

    os.system("xcopy " + binario_atualizado + " " + pasta_binario)

def renomear_appserver(pasta_binario, nome_exe):
    original = pasta_binario + "\\" + "appserver.exe"
    novo = pasta_binario + "\\" + nome_exe
    os.rename(original, novo)

def copia_ini(pasta_backup, pasta_binario, arquivo_ini):
    ini_backup = pasta_backup + "\\" + arquivo_ini
    ini_binario = pasta_binario + "\\" + arquivo_ini
    os.system("copy " + ini_backup + " " + ini_binario)

def ajusta_arquivo_ini(pasta_binario, appserver_ini, ambiente, server_licenseclient , port_licenseclient):
    ini_binario = pasta_binario + "\\" + appserver_ini

    config = ConfigParser()
    config.read(ini_binario)

    rpo_custom = config[ambiente]["sourcepath"]
    rpo_custom += "\\apo_custom.rpo"

    config.set(ambiente, "RpoLanguage", "multi")

    config.set(ambiente, "RpoCustom", rpo_custom)

    if config.has_option(ambiente, "INACTIVETIMEOUT"):
        config.set(ambiente, "INACTIVETIMEOUT", "1200" )

    config.set("General", "consolemaxsize", "31457280")
    config.set("General", "maxstringsize", "10")

    config.set("LICENSECLIENT", "server", server_licenseclient)
    config.set("LICENSECLIENT", "port", port_licenseclient)

    config.set("DBAccess", "DataBase", "MSSQL")

    with open(ini_binario, 'w') as configfile:
        config.write(configfile)

def main():

    config = ConfigParser()
    config.read("atualiza_binario.ini")

    sessoes_bin = (config["atualiza_binario"]["execbinarios"]).split(',')
    binario_atualizado = config["atualiza_binario"]["binario_atualizado"]
    server_licenseclient = config["atualiza_binario"]["server_licenseclient"]
    port_licenseclient = config["atualiza_binario"]["port_licenseclient"]

    for sessao in sessoes_bin:

        continua_processo = False

        pasta_binario = config[sessao]["pasta_binario"]
        pasta_backup = config[sessao]["pasta_binario"].replace(
            sessao, "@backup" + sessao)

        appserver_exe = config[sessao]["appserver_exe"]
        appserver_ini = config[sessao]["appserver_ini"]

        ambiente = ""
        if config.has_section(sessao):
            if config.has_option(sessao, "ambiente"):
                ambiente = config[sessao]["ambiente"]

        if os.path.exists(pasta_binario):
            if os.path.exists(pasta_binario + "\\" + appserver_exe):
                if os.path.exists(pasta_binario + "\\" + appserver_ini):
                    continua_processo = True

        print("binario: " + pasta_binario)

        if continua_processo:
            # renomeia a pasta para criar um backup
            renomeia_pasta(pasta_binario, pasta_backup)
            sleep(0.5)

            # cria uma pasta com o nome da original
            cria_pasta(pasta_binario)
            sleep(0.5)

            # copia o novo binario
            copia_novo_binario(binario_atualizado,pasta_binario)
            sleep(0.5)

            # renomeia o APPSERVER para o nome correto do Servico
            renomear_appserver(pasta_binario, appserver_exe)
            sleep(0.5)

            # Copia o INI da pasta de Backup
            copia_ini(pasta_backup, pasta_binario, appserver_ini)
            sleep(0.5)

            # Cria/Altera a chave RPOCustomo
            if ambiente != "":
                ambientes = ambiente.split(',')
                for a in ambientes:
                    ajusta_arquivo_ini(pasta_binario, appserver_ini, a , server_licenseclient , port_licenseclient)
                    sleep(0.5)
        else:
            print("Pasta não existe")

        print("------------------------------")

if __name__ == "__main__":
    try:
        # main()
        print("main.py - desabilitado")
    except:

        hora_atual = datetime.now()
        hora_data_erro = hora_atual.strftime('%Y%m%d_%H%M%S')
        arquivo_erro = "error_log_" + hora_data_erro + ".log"
        f = open(arquivo_erro, "w")
        f.write(format_exc())
        f.close()
        print("PROBLEMA ENCONTRADO!!!")
        print(arquivo_erro)
        input()
