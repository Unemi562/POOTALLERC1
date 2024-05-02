from utilities import borrarPantalla, gotoxy
import time


class Menu:
    def __init__(self, titulo="", opciones=[], col=6, fil=1):
        self.titulo = titulo
        self.opciones = opciones
        self.col = col
        self.fil = fil
        
    def menu(self):
        print('\033c', end='') 
        
        print("\033[1;32m╔" + "═" * 52 + "╗\033[0m")  
        print("\033[1;32m║" + f"{self.titulo:^50}" + " ║\033[0m")  
        print("\033[1;32m╠" + "═" * 52 + "╣\033[0m")  
        for i, opcion in enumerate(self.opciones, start=1):
            print("\033[1;34m║" + f"{i}. {opcion:<48}" + " ║\033[0m")  
        print("\033[1;32m╚" + "═" * 52 + "╝\033[0m")  
        opc = input("\033[1;35m" + f"Elija opción[1...{len(self.opciones)}]: " + "\033[0m")  
        return opc
    
class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
        return valor


    def solo_letras(self, mensajeError,col,fil):
        while True:
            gotoxy(col,fil)
            valor = input().strip()
            valor = ''.join(valor.split()) 
            if valor and all(char.isalpha() or char.isspace() for char in valor):
                break
            else:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
                
        return valor
    
    def solo_letras_and_espacios(self, mensajeError, col, fil, valor_actual=None):
            while True:
                gotoxy(col, fil)
                valor = input().strip()  
                valor_sin_espacios = ''.join(valor.split())
                if not valor_sin_espacios:  
                    if valor_actual is not None:  
                        return valor_actual
                    else:  
                        gotoxy(col, fil); print(mensajeError)
                        time.sleep(1)
                        gotoxy(col, fil); print(" " * 30)
                else:
                    if all(char.isalpha() or char.isspace() for char in valor_sin_espacios):
                        return valor_sin_espacios
                gotoxy(col, fil); print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil); print(" " * 30)
        

    def solo_decimales(self,mensajeError,col,fil):
        while True:
            gotoxy(col,fil)
            valor = str(input())
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
        return valor
    
    def solo_decimales_and_espacios(self, mensajeError, col, fil, valor_actual=None):
        while True:
            gotoxy(col, fil)
            valor = input().strip() 
            if not valor:  
                if valor_actual is not None:  
                    return valor_actual
                else:  
                    gotoxy(col, fil); print(mensajeError)
                    time.sleep(1)
                    gotoxy(col, fil); print(" " * 30)
            else:
                try:
                    valor = float(valor)
                    if valor > 0:
                        return valor
                except ValueError:
                    pass
                gotoxy(col, fil); print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil); print(" " * 30)
    
    def cedula(self,mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            cedula = input()
            if len(cedula) == 10 and cedula.isdigit():
                break
            else:
                gotoxy(col, fil)
                print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*25)
        return cedula

class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)
