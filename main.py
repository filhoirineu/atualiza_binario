from lib2to3.pygram import python_grammar_no_print_statement
import os
from time import sleep
from configparser import ConfigParser
from traceback import format_exc
from datetime import datetime
from termcolor import *
from art import text2art
import ctypes

def pula_linha(x):
    print("\n" * x)

def mensagem_funcao(mensagem=""):
    cprint(mensagem, 'cyan', attrs=['bold'])

def mensagem_erro(mensagem=""):
    cprint(mensagem, 'red', attrs=['bold'])
    input("")

def mensagem_sucesso(mensagem=""):
    cprint(mensagem, 'green', attrs=['bold'])

def mensagem_info(mensagem=""):
    cprint(mensagem, attrs=['bold'])

def renomeia_pasta(antes, depois):
    os.rename(antes, depois)

def cria_pasta(nova_pasta):
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)

def copia_novo_binario(binario_atualizado,pasta_binario):

    os.system("xcopy " + binario_atualizado + " " + pasta_binario)

def renomear_appserver_exe(pasta_binario, nome_exe):
    original = pasta_binario + "\\" + "appserver.exe"
    novo = pasta_binario + "\\" + nome_exe
    os.rename(original, novo)

def copia_ini(pasta_backup, pasta_binario, arquivo_ini):
    ini_backup = pasta_backup + "\\" + arquivo_ini
    ini_binario = pasta_binario + "\\" + arquivo_ini
    os.system("copy " + ini_backup + " " + ini_binario)

def ajusta_arquivo_ini(pasta_binario, appserver_ini, ambiente):
    ini_binario = pasta_binario + "\\" + appserver_ini

    config = ConfigParser()
    config.read(ini_binario)

    if config.has_option(ambiente, "INACTIVETIMEOUT"):
        config.set(ambiente, "INACTIVETIMEOUT", "1800" )

    config.set("General", "consolemaxsize", "25000000")
    config.set("General", "maxstringsize", "15")

    with open(ini_binario, 'w') as configfile:
        config.write(configfile)

def program_logo():
    cprint(text2art("atualiza".center(10), font="charact1"), "green", attrs=['bold'])
    cprint(text2art("binario".center(10), font="charact1"), "green", attrs=['bold'])

def finalizado():
    cprint(text2art("processo".center(12), font="charact1"), "green", attrs=['bold'])
    cprint(text2art("finalizado".center(12), font="charact1"), "green", attrs=['bold'])
    input()

def abortado():
    cprint(text2art("processo".center(12), font="charact1"), "red", attrs=['bold'])
    cprint(text2art("abortado".center(12), font="charact1"), "red", attrs=['bold'])
    input()

def processa_programa():

    pula_linha(3)

    resposta = input(colored("DESEJA CONTINUAR (SIM/NAO) ?   ", 'yellow', attrs=['bold']))

    if resposta.upper() in "S/SIM":
        return True
    else:
        return False

def main():

    config = ConfigParser()
    config.read("atualiza_binario.ini")

    sessoes_bin = config["atualiza_binario"]["execbinarios"]
    binario_atualizado = config["atualiza_binario"]["binario_atualizado"]

    program_logo()
    mensagem_info("SESSÕES A SEREM ATUALIZADAS: " + sessoes_bin)
    pula_linha(2)
    mensagem_info("BINÁRIO ATUALIZADO: " + binario_atualizado)

    if processa_programa():

        sessoes_bin = (config["atualiza_binario"]["execbinarios"]).split(',')

        os.system("cls")
        program_logo()

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

            mensagem_funcao(pasta_binario)
            pula_linha(1)
            sleep(1)

            if continua_processo:
                # renomeia a pasta para criar um backup
                mensagem_funcao("renomeia_pasta")
                sleep(0.3)
                renomeia_pasta(pasta_binario, pasta_backup)


                # cria uma pasta com o nome da original
                mensagem_funcao("cria_pasta")
                sleep(0.3)
                cria_pasta(pasta_binario)


                # copia o novo binario
                mensagem_funcao("copia_novo_binario")
                sleep(0.3)
                copia_novo_binario(binario_atualizado,pasta_binario)

                # renomeia o APPSERVER para o nome correto do Servico
                pula_linha(1)
                mensagem_funcao("renomear_appserver_exe")
                sleep(0.3)
                renomear_appserver_exe(pasta_binario, appserver_exe)

                # Copia o INI da pasta de Backup
                pula_linha(2)
                mensagem_funcao("copia_ini")
                sleep(0.3)
                copia_ini(pasta_backup, pasta_binario, appserver_ini)

                # Cria/Altera a chave RPOCustomo
                if ambiente != "":
                    ambientes = ambiente.split(',')
                    for a in ambientes:
                        pula_linha(1)
                        mensagem_funcao("ajusta_arquivo_ini")
                        sleep(0.3)
                        ajusta_arquivo_ini(pasta_binario, appserver_ini, a)

            else:
                mensagem_erro("PASTA NÃO EXISTE")


            pula_linha(2)
            print("------------------------------")

        finalizado()

    else:
        abortado()


if __name__ == "__main__":
    try:

        os.system('mode con: cols=125 lines=50')
        ctypes.windll.kernel32.SetConsoleTitleW("ATUALIZA BINARIO by: @filhoirineu")
        os.system('cls')
        if os.path.exists("atualiza_binario.ini"):
            main()
        else:
            mensagem_erro("atualiza_binario.ini NÃO ENCONTRADO!!!")


    except:

        hora_atual = datetime.now()
        hora_data_erro = hora_atual.strftime('%Y%m%d_%H%M%S')
        arquivo_erro = "error_log_" + hora_data_erro + ".log"
        f = open(arquivo_erro, "w")
        f.write(format_exc())
        f.close()
        mensagem_erro("PROBLEMA ENCONTRADO!!!")
        mensagem_erro(arquivo_erro)
        input()
