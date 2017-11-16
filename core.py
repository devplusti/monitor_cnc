from os import system
import I2C_LCD_driver
import RPi.GPIO as GPIO
import time
from pad4pi import rpi_gpio
from datetime import datetime

#########################################################################
def LimpaDisplay(lin=0):
#########################################################################
    if lin >= 1:
       lcd.lcd_display_string("                ", lin,0)
    else:
       lcd.lcd_clear()

#########################################################################
def acendeled(pino_led):
#########################################################################
    GPIO.output(pino_led, 1)

    return

#########################################################################
def apagaled(pino_led):
#########################################################################
    GPIO.output(pino_led, 0)

    return

#########################################################################
def key_pressed(key):
#########################################################################
    global TextoEntradaTeclado
    global pressedkey

    pressedkey = str(key)

#########################################################################
def ordem_producao_aberta():
#########################################################################
    Retorno = True

    for i in ordem_producao:
        if not ordem_producao[i]:
            Retorno = False
            break

    return Retorno

#########################################################################
def abertura_producao(nModo):
#########################################################################
    operador = ""
    op = ""
    operacao = ""

    LimpaDisplay()
    if nModo == 1:  # ORDEM PRODUCAO
        label = "OPERADOR"
        titulo = "PRODUCAO"

    elif nModo == 2: # SETUP
        label = "PROGRAMAD"
        titulo = "SETUP"

    elif nModo == 3: # Controle de Qualidade
         label = "INSPETOR"
         titulo = "LIBERACAO"

    if ordem_producao_aberta():
        lcd.lcd_display_string("ORDEM DE "+titulo, 1,0)
        lcd.lcd_display_string("JA FOI ABERTA !!!", 2,0)
        time.sleep(0.5)

        return

    if len(operador) == 0:
       ordem_producao["operador"] = pega_dados_ordem_producao(label,3,1,titulo)

    if len(op) == 0:
       ordem_producao["op"] = pega_dados_ordem_producao("OP",6,1,titulo)

    if len(operacao) == 0:
       ordem_producao["operacao"] = pega_dados_ordem_producao("OPERACAO",3,1,titulo)

    #Gravar Abertura da OP
    gravar_dados(nModo)


#########################################################################
def encerramento_producao(nModo):
#########################################################################
    operador = ""
    op = ""
    operacao = ""

    if nModo == 1:  # ORDEM PRODUCAO
        label = "OPERADOR"
        titulo = "PRODUCAO"

    elif nModo == 2: # SETUP
        label = "PROGRAMADOR"
        titulo = "SETUP"

    elif nModo == 3: # Controle de Qualidade
         label = "INSPETOR"
         titulo = "LIBERACAO"

    if not ordem_producao_aberta():
       LimpaDisplay()
       lcd.lcd_display_string("ORDEM DE PRODUCAO", 1,0)
       lcd.lcd_display_string("NAO FOI ABERTA !", 2,0)
       time.sleep(0.5)
       LimpaDisplay()

       return

    if nModo == 1:
        #LimpaDisplay()

        if len(operador) == 0:
           aux = pega_dados_ordem_producao("OPERADOR",3,2,titulo)
           if ordem_producao["operador"] != aux:
               print("OPERADOR DIFERENTE",ordem_producao,aux)
               LimpaDisplay()
               lcd.lcd_display_string("OPERADOR DIFERENTE", 1,0)
               time.sleep(3)

               LimpaDisplay()
               return

        if len(op) == 0:
           aux = pega_dados_ordem_producao("OP",6,2,titulo)
           if ordem_producao["op"] != aux:
               print("OP DIFERENTE",ordem_producao,aux)
               LimpaDisplay()
               lcd.lcd_display_string("OP DIFERENTE", 1,0)
               time.sleep(3)

               LimpaDisplay()
               return

        if len(operacao) == 0:
           aux = pega_dados_ordem_producao("OPERACAO",3,2,titulo)
           if ordem_producao["operacao"] != aux:
               print("OPERACAO DIFERENTE",ordem_producao,aux)
               LimpaDisplay()
               lcd.lcd_display_string("OPERACAO DIFERENTE", 1,0)
               time.sleep(3)

               LimpaDisplay()
               return

    #Gravar Encerramento da OP
    gravar_dados(2)

    ordem_producao["operador"] = ""
    ordem_producao["op"] = ""
    ordem_producao["operacao"] = ""


#########################################################################
def pega_dados_ordem_producao(texto_display,tamanho,modo,titulo):
#########################################################################
    global TextoEntradaTeclado
    global pressedkey

    if modo == 1:
        modo_texto = "ABERTURA"
    elif modo == 2:
        modo_texto = "ENCERRAMENTO"
    elif modo == 3:
        modo_texto = "MOTIVO"

    TextoEntradaTeclado = ""
    pressedkey = ""
    sair = False
    operador = ""

    texto_display_original = texto_display
    texto_display = texto_display + ": "

    while True:
        lcd.lcd_display_string(modo_texto+" "+titulo, 1,0)
        lcd.lcd_display_string(texto_display, 2,0)

        print(texto_display)
        print(TextoEntradaTeclado)

        if pressedkey == "#" or len(TextoEntradaTeclado) == tamanho:
            operador += TextoEntradaTeclado
            pressedkey = ""
            LimpaDisplay()
            lcd.lcd_display_string(texto_display_original+" "+operador+"?", 1,0)
            lcd.lcd_display_string("CONF(#)||CANC(*)", 2,0)

            while True:
                if pressedkey == "#":
                    LimpaDisplay()
                    lcd.lcd_display_string("CONFIRMADO !!!", 1,0)
                    time.sleep(1)

                    pressedkey = ""
                    LimpaDisplay()

                    sair = True
                    break
                elif pressedkey == "*":
                    texto_display = texto_display_original+": "
                    TextoEntradaTeclado = ""
                    pressedkey = ""
                    operador = ""
                    LimpaDisplay()

                    sair = False
                    break

            if sair:
                break

        else:
           texto_display += pressedkey
           TextoEntradaTeclado += pressedkey
           pressedkey = ""

    return operador

#########################################################################
def gravar_dados(modo=0):
#########################################################################

    # modo = 0 operacao normal
    # modo = 1 abertura op
    # modo = 2 encerramento op
    # modo = 3 paradas

    if modo == 1:
        cabec = 'data, hora,'+\
                 'op,'+\
                 'operador,'+\
                 'operacao,'+\
                 'modo,'+\
                 'qtd_pecas,'+\
                 'estado_maquina,'+\
                 'codigo_de_parada'
    else:
        cabec = ''

    string = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")+','+\
             ordem_producao["op"]+','+\
             ordem_producao["operador"]+','+\
             ordem_producao["operacao"]+','+\
             str(modo)+','+\
             str(qtd_pecas)+','+\
             str(estado_maquina)+','+\
             str(codigo_de_parada)

    arq = open("maq001.txt", "a")
    if cabec:
        arq.write(cabec+"\n")

    arq.write(string+"\n")
    arq.close()

    print(string)

#########################################################################
def solicitar_motivo_maq_parada():
#########################################################################
    LimpaDisplay()
    codigo_de_parada = pega_dados_ordem_producao("CODIGO",2,3,"PARADA")

    #Gravar Abertura da OP
    gravar_dados(3)

    return (codigo_de_parada)

#########################################################################
# PROGRAMA PRINCIPAL                                                    #
#########################################################################
global ordem_producao
global codigo_de_parada

cDescricaoEstadoMaquina = ""

TextoEntradaTeclado = ""
key = 0
pressedkey = ""

lAberturaOP = False

led1 = 0
qtd_pecas = 0
total_pecas = 0

# INSTANCIANDO O DISPLAY
lcd = I2C_LCD_driver.lcd()

estadoantigo0 = 1
estado_atual_peca = 0
estadoantigo1 = 1
estado_maquina = 0
estadoantigo2 = 1
codigo_de_parada = 0

pinoLED = 26
pinoBtnPeca = 20
pinoBtnSetup = 12
pinoBtnEstadoMaq = 27

#Exibe informacoes iniciais
lcd.lcd_display_string("Cipec Industrial", 1,0)
lcd.lcd_display_string("de Autopecas", 2,2)
time.sleep(2)

#Apaga o display
lcd.lcd_clear()

#inicializando as funcoes do led
tempo_limite_maq_parada = 10 # segundos
TempoLiga = 1 # segundo
TempoDesliga = 1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinoLED, GPIO.OUT)
GPIO.setup(pinoBtnPeca, GPIO.IN)
GPIO.setup(pinoBtnSetup, GPIO.IN)
GPIO.setup(pinoBtnEstadoMaq, GPIO.IN)

ordem_producao = {"operador": "","op": "","operacao":""}
codigo_de_parada = 0
contador_tempo_maq_parada = 0

# SETAGEM TECLADO 4x4
keypad = [
         [1  ,2 ,3  ,"A"],
         [4  ,5 ,6  ,"B"],
         [7  ,8 ,9  ,"C"],
         ["*",0 ,"#","D"]
         ]

row_pins = [4,17,21,22] # BCM numbering
col_pins = [18,23,24,25] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad, row_pins, col_pins)
keypad.registerKeyPressHandler(key_pressed)
teclas_extra = ''

while(1):
    if led1 == 0:
       acendeled(pinoLED)
       led1=1

    if led1 == 1:
       apagaled(pinoLED)
       led1=0

    print(ordem_producao," te ",pressedkey," st ",estado_maquina, 'TE', teclas_extra)
    print("codigo parada",codigo_de_parada)
    print("MAQ PARADA: "+str(contador_tempo_maq_parada).zfill(3))

    # MAQUINA PARADA
    if estado_maquina == 0:
        # Verifica se a tecla A ABERTURA
        if pressedkey == "A" and estado_maquina == 0:
           pressedkey = ""
           abertura_producao(1)

        # Verifica se a tecla B ENCERRAMENTO
        if pressedkey == "B":
           pressedkey = ""
           encerramento_producao(1)

        # Verifica se a tecla C SETUP
        if pressedkey == "C":
           pressedkey = ""
           abertura_producao(2)

        # Verifica se a tecla D INSPECAO CONTROLE QUALIDADE
        if pressedkey == "D":
           pressedkey = ""
           abertura_producao(3)
    else:
        pressedkey = ""

    # Verifica se ordem producao ja foi aberta
    if not ordem_producao_aberta():
        #LimpaDisplay()
        lcd.lcd_display_string("ORDEM PRODUCAO", 1,0)
        lcd.lcd_display_string("FECHADA !!!", 2,0)

        time.sleep(0.5)

        teclas_extra = teclas_extra + pressedkey

        if len(teclas_extra) == 3:
            if teclas_extra == '999':
                lcd.lcd_display_string("ENCERRANDO O  ", 1,0)
                lcd.lcd_display_string("PROGRAMA !!!  ", 2,0)
                time.sleep(1)

                #os.system("shutdown -t 0 -h")
                lcd.backlight(0)

                exit()
            else:
                teclas_extra = ''

        continue # RETORNA PARA O INICIO DO WHILE

    # botao conta-peca
    if  GPIO.input(pinoBtnPeca) == 1 and estado_maquina != 0:
        estado_atual_peca = 1

        if estadoantigo0 == 0:
            estadoantigo0 = 1
            qtd_pecas = 1
            total_pecas = total_pecas + 1
            gravar_dados(0)

    if  GPIO.input(pinoBtnPeca) == 0:
        estadoantigo0 = 0
        qtd_pecas = 0

    #botao estado da maquina
    if  GPIO.input(pinoBtnEstadoMaq) == 1:
        estado_maquina = 1
        cDescricaoEstadoMaquina = "EM OPERACAO"
        codigo_de_parada = 0

        if estadoantigo1 == 0:
           estadoantigo1 = 1
           gravar_dados(0)

    if GPIO.input(pinoBtnEstadoMaq) == 0:
        estado_maquina = 0
        cDescricaoEstadoMaquina = "MAQUINA PARADA"

        if contador_tempo_maq_parada == 0:
            hora_inicial_maq_parada = time.time()

        if estadoantigo1 == 1:
           estadoantigo1 = 0
           contador_tempo_maq_parada = 0
           gravar_dados(0)

        contador_tempo_maq_parada = contador_tempo_maq_parada + 1

        if codigo_de_parada == 0 and (time.time() - hora_inicial_maq_parada) > tempo_limite_maq_parada:
           codigo_de_parada = solicitar_motivo_maq_parada()
           contador_tempo_maq_parada = 0

    #botao de setup
    if  GPIO.input(pinoBtnSetup) == 1:
        codigo_de_parada = 1
        cDescricaoEstadoMaquina = "EM SETUP"

        if estadoantigo2 == 0:
           estadoantigo2 = 1
           gravar_dados(0)

    if GPIO.input(pinoBtnSetup) == 0:
        codigo_de_parada = 0

        if estadoantigo2 == 1:
           estadoantigo2 = 0
           gravar_dados(0)

    #DISPLAY
    #LimpaDisplay()
    lcd.lcd_display_string(cDescricaoEstadoMaquina, 1,0)
    if estado_maquina == 1: # MAQ EM OPERACAO
       lcd.lcd_display_string("QTD:"+str(total_pecas)+" OP:"+str(ordem_producao["op"]).zfill(7), 2,0)

    if estado_maquina == 0:
        if codigo_de_parada == 0:
           lcd.lcd_display_string("HORA INI: "+time.strftime("%H:%M",time.localtime(hora_inicial_maq_parada)), 2,0)
        else:
           lcd.lcd_display_string("COD: "+str(codigo_de_parada), 2,0)

        contador_tempo_maq_parada = contador_tempo_maq_parada + 1
