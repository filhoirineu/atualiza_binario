from lib2to3.pygram import python_grammar_no_print_statement
import os
from time import sleep
from configparser import ConfigParser
from traceback import format_exc
from datetime import datetime
from termcolor import *
from art import text2art
import ctypes

ID_ROTINA = ""

def pula_linha(x):
    print("\n" * x)

def msg_funcao(mensagem=""):
    cprint(mensagem, 'cyan', attrs=['bold'])

def msg_sub_msg(subtitulo="",mensagem=""):
    print(colored(subtitulo,'cyan',attrs=['bold']) + mensagem)

def msg_erro(mensagem=""):
    cprint(mensagem, 'red', attrs=['bold'])
    input("")

def msg_sucesso(mensagem=""):
    cprint(mensagem, 'green', attrs=['bold'])

def msg_info(mensagem=""):
    cprint(mensagem, attrs=['bold'])

def renomeia_pasta(antes, depois):
    os.rename(antes, depois)

def cria_pasta(nova_pasta):
    if not os.path.exists(nova_pasta):
        os.makedirs(nova_pasta)

def copia_novo_binario(binario_atualizado, pasta_binario):

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
        config.set(ambiente, "INACTIVETIMEOUT", "1800")

    config.set("General", "consolemaxsize", "50000000")
    config.set("General", "maxstringsize", "10")

    with open(ini_binario, 'w') as configfile:
        config.write(configfile)

def program_logo():
    cprint(text2art("atualiza".center(10), font="charact1"),
           "green", attrs=['bold'])
    cprint(text2art("binario".center(10), font="charact1"),
           "green", attrs=['bold'])

def finalizado():
    cprint(text2art("finalizado".center(12), font="charact1"),
           "green", attrs=['bold'])
    input()

def abortado():
    cprint(text2art("processo".center(12), font="charact1"),
           "red", attrs=['bold'])
    cprint(text2art("abortado".center(12), font="charact1"),
           "red", attrs=['bold'])
    input()

def processa_programa():

    pula_linha(3)

    resposta = input(
        colored("DESEJA CONTINUAR (SIM/NAO) ?   ", 'yellow', attrs=['bold']))

    if resposta.upper() in "S/SIM":
        return True
    else:
        return False

def main():

    config = ConfigParser()
    config.read("atualiza_binario.ini")

    ID_ROTINA = datetime.now().strftime('%Y%m%d_%H%M%S')

    sessoes_bin = config["atualiza_binario"]["execbinarios"]
    binario_atualizado = config["atualiza_binario"]["binario_atualizado"]

    program_logo()
    msg_sub_msg("SESSÕES A SEREM ATUALIZADAS: " , sessoes_bin)
    pula_linha(2)
    msg_sub_msg("BINÁRIO ATUALIZADO: " , binario_atualizado)

    if processa_programa():

        sessoes_bin = (config["atualiza_binario"]["execbinarios"]).split(',')

        os.system("cls")
        pula_linha(2)

        for sessao in sessoes_bin:

            continua_processo = False

            pasta_binario = config[sessao]["pasta_binario"]
            pasta_backup = config[sessao]["pasta_binario"].replace(
                sessao, "@backup_" + ID_ROTINA + "_" + sessao)

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

            msg_funcao(pasta_binario)
            msg_funcao(ambiente)
            pula_linha(1)
            sleep(0.5)

            if continua_processo:
                # renomeia a pasta para criar um backup
                msg_funcao("renomeia_pasta")
                msg_sub_msg("pasta_binario: " , pasta_binario)
                msg_sub_msg("pasta_backup: " , pasta_backup)
                sleep(0.1)
                renomeia_pasta(pasta_binario, pasta_backup)

                pula_linha(1)

                # cria uma pasta com o nome da original
                msg_funcao("cria_pasta")
                msg_sub_msg("pasta_binario: " , pasta_binario)
                sleep(0.1)
                cria_pasta(pasta_binario)

                pula_linha(1)

                # copia o novo binario
                msg_funcao("copia_novo_binario")
                msg_sub_msg("binario_atualizado: " , binario_atualizado)
                msg_sub_msg("pasta_binario: " , pasta_binario)
                sleep(0.1)
                copia_novo_binario(binario_atualizado, pasta_binario)

                pula_linha(1)

                # renomeia o APPSERVER para o nome correto do Servico
                pula_linha(1)
                msg_funcao("renomear_appserver_exe")
                msg_sub_msg("pasta_binario: " , pasta_binario)
                msg_sub_msg("appserver_exe: " , appserver_exe)
                sleep(0.1)
                renomear_appserver_exe(pasta_binario, appserver_exe)

                pula_linha(1)

                # Copia o INI da pasta de Backup
                pula_linha(2)
                msg_funcao("copia_ini")
                msg_sub_msg("pasta_backup: " , pasta_backup)
                msg_sub_msg("pasta_binario: " , pasta_binario)
                msg_sub_msg("appserver_ini: " , appserver_ini)
                sleep(0.1)
                copia_ini(pasta_backup, pasta_binario, appserver_ini)

                pula_linha(1)

                # Cria/Altera a chave RPOCustomo
                if ambiente != "":
                    ambientes = ambiente.split(',')
                    for ambiente in ambientes:
                        pula_linha(1)
                        msg_funcao("ajusta_arquivo_ini")
                        msg_sub_msg("pasta_binario: " , pasta_binario)
                        msg_sub_msg("appserver_ini: " , appserver_ini)
                        msg_sub_msg("ambiente: " , ambiente)
                        sleep(0.1)
                        ajusta_arquivo_ini(
                            pasta_binario, appserver_ini, ambiente)

            else:
                msg_erro("PASTA NÃO EXISTE")

            pula_linha(2)
            print("------------------------------")

        finalizado()

    else:
        abortado()

if __name__ == "__main__":
    try:

        os.system('mode con: cols=125 lines=50')
        ctypes.windll.kernel32.SetConsoleTitleW(
            "ATUALIZA BINARIO by: @filhoirineu")
        os.system('cls')
        if os.path.exists("atualiza_binario.ini"):
            main()
        else:
            msg_erro("atualiza_binario.ini NÃO ENCONTRADO!!!")

    except:

        hora_atual = datetime.now()
        hora_data_erro = hora_atual.strftime('%Y%m%d_%H%M%S')
        arquivo_erro = "error_log_" + hora_data_erro + ".log"
        f = open(arquivo_erro, "w")
        f.write(format_exc())
        f.close()
        msg_erro("PROBLEMA ENCONTRADO!!!")
        msg_erro(arquivo_erro)
        input()
