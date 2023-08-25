#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        comando_1 = b'\x00\x00\x00\x00'
        comando_2 = b'\x00\x00\xBB\x00'
        comando_3 = b'\xBB\x00\x00'
        comando_4 = b'\x00\xBB\x00'
        comando_5 = b'\x00\x00\xBB'
        comando_6 = b'\x00\xAA'
        comando_7 = b'\xBB\x00'
        comando_8 = b'\x00'
        comando_9 = b'\xBB'
        comandos = [comando_1, comando_2, comando_3, comando_4, comando_5, comando_6, comando_7, comando_8, comando_9]

        N = random.randint(10, 30)

        comandos_a_serem_enviados = []
        tamanho_comandos_a_serem_enviados = []

        i = 0
        while i < N:
            comandos_a_serem_enviados.append(random.choice(comandos))
            tamanho_comandos_a_serem_enviados.append(int.to_bytes(len(random.choice(comandos))))
            i += 1

        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        print ("A transmissão vai começar")

        com1.enable()
        time.sleep(.2)
        com1.sendData(b'11')
        time.sleep(1)
        
        i = 0
        while i < len(comandos_a_serem_enviados):
            com1.sendData(np.asarray(tamanho_comandos_a_serem_enviados[i]))
            com1.sendData(np.asarray(comandos_a_serem_enviados[i]))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
            while com1.tx.getIsBussy():
                pass
            #com1.sendData(b'11')
            time.sleep(1)
            i += 1



        time.sleep(5)

        rxBuffer, nRx = com1.getData(txLen)
        
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        
        """
        txSize = 0
        while com1.tx.transLen < len(txBuffer):
            time.sleep(2) 
        """

        while com1.tx.getIsBussy():
            pass

        txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        print ("Salvando dados no arquivo :")
        print(" - {}".format(imageW))
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com1.getData(txLen)
        
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
        
        f = open(imageW, 'wb')
        f.write(rxBuffer)

        # Fecha arquivo de imagem
        f.close()
        
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
