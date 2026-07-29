"""
Módulo da Camada Física (Interface Hardware).
Responsável pela comunicação assíncrona full-duplex com o microcontrolador ESP32
através da interface série (UART/USB).
"""
import serial
import threading

class Camada2_FullDuplex: 
    def __init__(self, porta_com: str, baudrate: int = 9600): 
        self.serial_port = serial.Serial(porta_com, baudrate, timeout=0.1) 
        self.running = False 
        self.rx_thread = None 
        # Buffer FIFO para as tramas lidas do canal
        self.tramas_recebidas = [] 

    def iniciar(self): 
        """Inicia a thread que fica a ler a porta série em background."""
        self.running = True 
        self.rx_thread = threading.Thread(target=self._receber_continuamente, daemon=True)  #loop em background
        self.rx_thread.start() 
        print(f"[Camada Física] Interface ativada na porta {self.serial_port.name} a {self.serial_port.baudrate} bps.") 

    def parar(self): 
        """Encerra a comunicação e liberta os recursos de hardware."""
        self.running = False 
        if self.rx_thread: 
            self.rx_thread.join() 
        self.serial_port.close() 
        print("[Camada Física] Conexão terminada com segurança.") 

    def enviar_trama_fisica(self, pacote_fisico: bytes): 
        """Escreve os bytes diretamente no hardware (porta série)."""    
        self.serial_port.write(pacote_fisico) 
        self.serial_port.flush() 

    def _receber_continuamente(self): 

        """Lê os bytes que chegam da porta série um a um e agrupa-os em tramas usando a flag SOF."""
        buffer_rx = bytearray() 
        em_rececao = False 
        SOF = b'\x7E'

        while self.running: 
            if self.serial_port.in_waiting > 0: 
                byte_lido = self.serial_port.read(1) 
            
                if byte_lido == SOF:                                                 ###### camada fisica nao deve ler o byte sof
                    # Encontrou um SOF (Início/Fim de trama)
                    # Se já tínhamos dados no buffer, significa que a trama terminou.
                    if len(buffer_rx) > 0: 
                        self.tramas_recebidas.append(bytes(buffer_rx)) 
                    
                    # Limpar o buffer para começar a ler a próxima trama
                    buffer_rx.clear() 
                    em_rececao = True 
                    
                else: 
                    # Adicionar o byte lido ao buffer da trama atual
                    if em_rececao: 
                        buffer_rx.extend(byte_lido)
                        
                        
## nao sabes onde a trama acaba! 