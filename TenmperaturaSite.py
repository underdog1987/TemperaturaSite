#! /usr/bin/env python
import serial
import string
import sys
import urllib2
import json
import time
from random import randint

URL_MSG_SEND = "https://your-microsoft-flow-url.com"


# Defs
# Envia lectura de sensores, pasar arg ya en json
def _sendMessage(soobshcheniye):
        data2 = json.dumps(soobshcheniye)
        headers = {'Content-Type': 'application/json', 'Content-Length': len(data2), 'User-Agent':'Raspberry Pi'}
        req = urllib2.Request(URL_MSG_SEND, data2, headers)
        response=urllib2.urlopen(req)
        return response.read() # Nada, porque la respuesta en Flow cuesta varo
########


ser = serial.Serial("/dev/ttyUSB0",9600)
lastMessage=""
# Valores obtenidos de los sensores
realTempC = 999 # Promedio
realTempLM35 = 999 # LM35
realTempLM335 = 999 # LM335
cuentaHora=0

while True:
        try:
                # Obtener info del entorno
                if ser.inWaiting():
                        valores = ser.readline()
                        # Los valores se entregan con la siguiente sintaxis:
                        # T=22.46|H=99.90|I=255
                        arValores=valores.split("|")
                        temp_ = arValores[2]
                        LM335_ = arValores[0]
                        LM35_ = arValores[1]

                        # Convertirt los strings de valores a float (luz a entero)
                        realTempC = float(temp_.strip())
                        realTempLM335 = float(LM335_.strip())
                        realTempLM35 = float(LM35_.strip())
                        #print valores

                        print "LM35:     " + str(realTempLM35)
                        print "LM335:    " + str(realTempLM335)
                        print "Promedio: " + str(realTempC)
                        print "========================================"
                        print "Enviar lectura en " + str(3600 - cuentaHora) + " segundos"
                        print " "
                else:
                        print "[ ! ] No Serial Data"
                time.sleep(1)
                cuentaHora = cuentaHora + 1
                if cuentaHora == 3600:
                        jsonTemp = {'nuTemperatura': int(realTempC), 'nuLM335': int(realTempLM335), 'nuLM35': int(realTempLM35)}
                        print "[ ! ] Sending HTTP request..."
                        _sendMessage(jsonTemp)
                        cuentaHora=0

        except KeyboardInterrupt:
                print '[ ! ] Cerrando....' # Debug only
                ser.close()
                sys.exit(1)
        except Exception as e:
                print str(e)
                pass

