from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color,white_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
from customer import RegularClient, VipClient


path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        print('\033c', end='')
        print(green_color + "*" * 92 + "\033[0m")
        print(green_color + "*\033[1m" + " " * 34 + "Creación de Cliente" + " " * 34 + "\033[0m" + green_color + "*\033[0m")
        print(green_color + "*" * 92 + "\033[0m")

        print(yellow_color + "*\033[1m" + "Ingrese el DNI:".ljust(27) + "\033[0m" + green_color + "*\033[0m", end="")
        dni = validar.cedula("Error: Cédula Inválida", 45, 4)
        json_file = JsonFile(path + '/archivos/clients.json')
        exists = json_file.find("dni", dni)
        if exists:
            print(green_color + "*\033[1m" + "Usuario ya existente".ljust(90) + "\033[0m" + green_color + "*\033[0m")
            time.sleep(2)
            return

        print(yellow_color + "*\033[1m" + "Ingrese su Nombre:".ljust(27) + "\033[0m" + green_color + "*\033[0m", end="")
        nombre = validar.solo_letras("Error: Solo Letras", 45, 5).capitalize()
        print(yellow_color + "*\033[1m" + "Ingrese su Apellido:".ljust(27) + "\033[0m" + green_color + "*\033[0m", end="")
        apellido = validar.solo_letras("Error: Solo Letras", 45, 6).capitalize()

        print(yellow_color + "*\033[1m" + "Es VIP? (s/n):".ljust(26) + "\033[0m" + green_color + "*\033[0m", end="")
        es_vip = validar.solo_letras("Error: Solo 's' o 'n' ", 45, 7).lower()
        if es_vip == "s" or es_vip == "si":
            valor = 10000
            cliente = VipClient(first_name=nombre, last_name=apellido, dni=dni)
            cliente.limit = valor
        else:
            print(yellow_color + "*\033[1m" + "¿Tiene tarjeta de descuento? (s/n):".ljust(42) + "\033[0m" + green_color + "*\033[0m", end="")
            tiene_tarjeta = validar.solo_letras("Error: Solo 's' o 'n' ", 89, 7).lower()
            if tiene_tarjeta == "s" or tiene_tarjeta == "si":
                card = True
            else:
                card = False
            cliente = RegularClient(first_name=nombre, last_name=apellido, dni=dni, card=card)
            valor = cliente.discount

        client = {"dni": dni,"nombre": nombre, "apellido": apellido, "valor": valor}

        if client['dni'] != "" and client['nombre'] != "" and client['apellido'] != "":
            print(yellow_color + "*\033[1mGuardar al Cliente presione (s/n):".ljust(42) + "\033[0m" + green_color + "*\033[0m", end="")
            valida = validar.solo_letras("Error: Solo 's' o 'n' ", 89, 9).lower()
            if valida == "s" or valida == "si":
                cli = json_file.read()
                clin = cli
                clin.append(client)
                json_file.save(clin)
                print(green_color + "*\033[1mCliente Agregado Con Éxito".ljust(90) + "\033[0m" + green_color + "*\033[0m")
                time.sleep(2)
            else:
                print(green_color + "*\033[1mAcción Eliminada".ljust(90) + "\033[0m" + green_color + "*\033[0m")
                time.sleep(1)
        else:
            print(green_color + "*\033[1mNo se llenaron los datos".ljust(90) + "\033[0m" + green_color + "*\033[0m")
            time.sleep(1)

        print(green_color + "*" * 92 + "\033[0m")

    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2, 1); print(purple_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 34 + yellow_color + "Actualizar Cliente" + " " * 35 + "██")
        print("Ingrese DNI del cliente a actualizar: ")
        gotoxy(2, 4); client_dni = validar.solo_numeros("Error: Solo números", 39, 3)
        json_file = JsonFile(path + '/archivos/clients.json')
        dato = json_file.read()
        clients = json_file.find("dni", client_dni)
        
        if not clients:
            print(red_color + f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            return
        
        client_index = None
        
        for idx, client in enumerate(dato):
            if client["dni"] == client_dni:
                client_index = idx
                break
        
        if client_index is not None:
            client = dato[client_index]
            valor_actual_nombre = client["nombre"]
            valor_actual_apellido = client["apellido"]
            gotoxy(15, 5); print("Cliente")
            gotoxy(35, 5); print("Apellido")
            gotoxy(55, 5); print("Valor")
            gotoxy(15, 6); print(f"{client['nombre']:}")
            gotoxy(35, 6); print(f"{client['apellido']}")
            gotoxy(55, 6); print(f"{client['valor']}")
            print("Ingrese el nuevo nombre (Deje vacío para mantener el mismo): ")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo letras", 62, 7, valor_actual_nombre).lower().capitalize()
            print("Ingrese el nuevo apellido (Deje vacío para mantener el mismo): ")
            new_apellido = validar.solo_letras_and_espacios("Error: Solo letras", 64, 8, valor_actual_apellido).lower().capitalize()
            print(yellow_color + "¿Quiere ser cliente VIP? (s/n): ", end="")
            tiene_tarjeta = validar.solo_letras("Error: Solo 's' o 'n' ", 32, 9).lower()
            
            if tiene_tarjeta == "s" or tiene_tarjeta == "si":
                cliente = VipClient(first_name=new_nombre, last_name=new_apellido, dni=client_dni)
                cliente.limit = 10000
            else:
                print(yellow_color + "¿Tiene tarjeta de descuento? (s/n): ", end="")
                tarjeta_descuento = validar.solo_letras("Error: Solo 's' o 'n' ", 37, 10).lower()
                if tarjeta_descuento == "si" or tarjeta_descuento == "s":
                    card = True
                else:
                    card = False
                cliente = RegularClient(first_name=new_nombre, last_name=new_apellido, dni=client_dni, card=card)
            
            dato[client_index] = cliente.getJson()
            json_file.save(dato)
            gotoxy(55, 13); print(green_color + "Cliente actualizado exitosamente.")
            time.sleep(2)
        else:
            print(red_color + f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        print("\033[1;35m█" + "█"*94 + "\033[0m") 
        print("\033[1;35m██" + " "*34 + "\033[1;36mEliminación de Cliente" + " "*35 + "██\033[0m")  
        print("\033[1;35mIngrese DNI del cliente a eliminar: \033[0m")  
        gotoxy(37, 4); client_dni = validar.solo_numeros("Error: Solo números", 37, 3)
        json_file = JsonFile(path+'/archivos/clients.json')
        dato = json_file.read()
        clients = json_file.find("dni", client_dni)
        
        for x in clients:
            if x["dni"] == client_dni:
                dato.remove(x)
                gotoxy(15, 5); print("\033[1;36mDNI\033[0m")  
                gotoxy(35, 5); print("\033[1;36mCliente\033[0m")
                gotoxy(55, 5); print("\033[1;36mApellido\033[0m")
                gotoxy(75, 5); print("\033[1;36mValor\033[0m")
                gotoxy(16, 6); print(f"{x['dni']:}")
                gotoxy(36, 6); print(f"{x['nombre']:}")
                gotoxy(56, 6); print(f"{x['apellido']}")
                gotoxy(37, 9); print("\033[1;36mCliente Eliminado\033[0m")  
                time.sleep(2)
                break
        else:
            print(f"\033[1;36mNo se encontró al cliente con el DNI: {client_dni}\033[0m")  
            time.sleep(1)
        json_file.save(dato)
        
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        print('\033[1;30m' + "█"*90)
        print('\033[1;30m' + "██" + " "*34 + "\033[1;32mConsulta de Cliente" + " "*35 + "██" + '\033[0m')
        print("¿Qué tipo de cliente desea consultar?")
        print("\033[1;32m1. VIP")
        print("2. Regular")
        print("3. Consultar a uno en específico:")
        print("4. Consultar Todos:")
        gotoxy(2, 9); print("\033[1;33mElija una opción:")
        tipo_cliente = validar.solo_numeros("Error: Ingrese 1, 2, 3 o 4", 23, 9)
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = []

        if tipo_cliente == "1":
            clients_vip = json_file.find("valor", 10000)
            clients.extend(clients_vip)
            gotoxy(15, 10); print('\033[1;34m' + "DNI" + '\033[0m')
            gotoxy(35, 10); print('\033[1;34m' + "Cliente" + '\033[0m')
            gotoxy(55, 10); print('\033[1;34m' + "Apellido" + '\033[0m')
            gotoxy(75, 10); print('\033[1;34m' + "Valor" + '\033[0m')
            linea = 0
            for client in clients:
                gotoxy(15, 11+linea); print(f"{client['dni']:}")
                gotoxy(36, 11+linea); print(f"{client['nombre']:}")
                gotoxy(56, 11+linea); print(f"{client['apellido']}")
                gotoxy(75, 11+linea); print(f"{client['valor']}")
                linea += 1
            gotoxy(2, 12+linea);input("Presione Enter para salir...")
        elif tipo_cliente == "2":
            clients_1 = json_file.find("valor", 0.1)
            clients_0 = json_file.find("valor", 0)
            clients.extend(clients_0)
            clients.extend(clients_1)
            gotoxy(15, 10); print('\033[1;34m' + "DNI" + '\033[0m')
            gotoxy(35, 10); print('\033[1;34m' + "Cliente" + '\033[0m')
            gotoxy(55, 10); print('\033[1;34m' + "Apellido" + '\033[0m')
            gotoxy(75, 10); print('\033[1;34m' + "Valor" + '\033[0m')
            linea = 0
            for client in clients:
                gotoxy(15, 11+linea); print(f"{client['dni']:}")
                gotoxy(36, 11+linea); print(f"{client['nombre']:}")
                gotoxy(56, 11+linea); print(f"{client['apellido']}")
                gotoxy(76, 11+linea); print(f"{client['valor']}")
                linea += 1
            gotoxy(2, 12+linea);input("Presione Enter para salir...")
        elif tipo_cliente == "3":
            json_file = JsonFile(path+'/archivos/clients.json')
            clients1 = json_file.read()
            print("Ingrese el DNI que desea consultar: ")
            gotoxy(2, 4); client = validar.solo_numeros("Error: Solo Numeros", 37, 10)
            for dni in clients1:
                if dni["dni"] == client:
                    gotoxy(15, 12); print('\033[1;34m' + "DNI" + '\033[0m')
                    gotoxy(35, 12); print('\033[1;34m' + "Cliente" + '\033[0m')
                    gotoxy(55, 12); print('\033[1;34m' + "Apellido" + '\033[0m')
                    gotoxy(75, 12); print('\033[1;34m' + "Valor" + '\033[0m')
                    gotoxy(15, 13); print(f"{dni['dni']:}")
                    gotoxy(36, 13); print(f"{dni['nombre']:}")
                    gotoxy(56, 13); print(f"{dni['apellido']}")
                    gotoxy(76, 13); print(f"{dni['valor']}")
                    gotoxy(2, 15);input("Presione Enter para salir...")
                    break
            else:
                print(f"No se encontró al cliente con el DNI: {client}")
            time.sleep(1)
        elif tipo_cliente == "4":
            json_file = JsonFile(path+'/archivos/clients.json')
            clients1 = json_file.read()
            linea = 0
            for dni in clients1:
                gotoxy(15, 10); print('\033[1;34m' + "DNI" + '\033[0m')
                gotoxy(35, 10); print('\033[1;34m' + "Cliente" + '\033[0m')
                gotoxy(55, 10); print('\033[1;34m' + "Apellido" + '\033[0m')
                gotoxy(75, 10); print('\033[1;34m' + "Valor" + '\033[0m')
                gotoxy(15, 11+linea); print(f"{dni['dni']:}")
                gotoxy(36, 11+linea); print(f"{dni['nombre']:}")
                gotoxy(56, 11+linea); print(f"{dni['apellido']}")
                gotoxy(76, 11+linea); print(f"{dni['valor']}")
                linea += 1
            gotoxy(2, 12+linea);input("Presione Enter para salir...")
        elif tipo_cliente not in ["1", "2", "3", "4"]:
            print("Opción no válida")
            
class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        print('\033c', end='')

        print(green_color + "*" * 92)
        print("*" + " " * 34 + "Crear Producto" + " " * 35 + "*")
        print("*" + green_color + "*" * 90 + "\033[0m")

        print(yellow_color + "Ingrese nombre del producto:" + green_color)
        gotoxy(2, 4)
        descripcion = validar.solo_letras("Error: Solo Letras", 30, 4).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        x_produt=json_file.find("descripcion",descripcion)

        if x_produt:
            print("Producto ya existente")
            time.sleep(1)
            return

        print(yellow_color + "Ingrese Precio:" + green_color)
        gotoxy(2, 5)
        precio = validar.solo_decimales("Error: Solo Numeros", 18, 5)

        print(yellow_color + "Ingrese Valor del Stock:" + green_color)
        gotoxy(2, 6)
        valo = validar.solo_decimales("Error: Solo Numeros", 26, 6)

        json_file = JsonFile(path + '/archivos/products.json')
        dato = json_file.read()
        ids = [producto["id"] for producto in dato if "id" in producto]
        ultimo_id = max(ids)
        Product.next = ultimo_id + 1
        nuevo_id = Product.next
        product = {"id": nuevo_id, "descripcion": descripcion, "precio": precio, "stock": valo}

        print("\n")
        print(green_color + "*" * 92)
        print(green_color + "*" + " ID " + green_color + "|" + " Descripcion " + green_color + "                  |" + " Precio " + green_color + "     |" + " Stock " + green_color + "   " + "*" + "\033[0m")
        print(green_color + "*" + "*" * 90 + "\033[0m")
        print(f"{product['id']:<8}| {product['descripcion']:<30} | {product['precio']:10} | {product['stock']:10}")

        time.sleep(2)

        if product['descripcion'] != "" and product['precio'] != "" and product["stock"]:
            print("\n")
            print(yellow_color + "Guardar el Producto presione (s/n)" + green_color)
            gotoxy(2, 11)  # Ajustamos la posición para que esté debajo de la solicitud
            valida = validar.solo_letras("Error: Solo Letras", 37, 11).lower()
            if valida == "s" or valida == "si":
                prod = json_file.read()
                prod.append(product)
                json_file.save(prod)
                gotoxy(56, 14)
                print(yellow_color + "El producto se guardo exitosamente" + green_color)
                time.sleep(2)
            else:
                gotoxy(24, 11)  # Ajustamos la posición para que esté al mismo nivel que la solicitud
                print(yellow_color + "Accion Eliminada" + green_color)
                time.sleep(1)
        else:
            print(yellow_color + "No se llenaron los datos" + green_color)
            time.sleep(1)
            
    def update(self):
        validar = Valida()
        print('\033c', end='')
        print("\033[95m" + "*" * 80)
        print("\033[95m*"*2 + " "*32 + "Actualizar Producto" + " "*33 + "\033[95m*"*2)
        print("\033[95m" + "*" * 80)

        print("\n\033[94m\033[1mIngrese el ID del Producto que desea actualizar:")
        producto_id = validar.solo_numeros("Error: Solo Números", 59, 5)
        producto_id = int(producto_id)
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        product = json_file.find("id", producto_id)

        if not product:
            print(f"\nNo se encontró el producto con el ID: {producto_id}")
            time.sleep(1)
            return

        producto_index = None

        for idx, products in enumerate(dato):
            if products["id"] == producto_id:
                producto_index = idx
                break

        if producto_index is not None:
            products = dato[producto_index]
            print("\n\033[94m\033[1mID\t\tDescripción\tPrecio\tStock")
            print(f"{products['id']}\t\t{products['descripcion']}\t\t{products['precio']}\t{products['stock']}")
            print("\n\033[91m\033[1mModificación del Nombre:")
            print("\033[94m\033[1mIngrese el nuevo nombre (Deje vacío para mantener el mismo): ")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo Letras", 62, 11, products['descripcion']).lower().capitalize()
            print("\n\033[94m\033[1mModificación del Precio:")
            print("\033[94m\033[1mIngrese el nuevo precio (Deje vacío para mantener el mismo): ")
            new_precio = validar.solo_decimales_and_espacios("Error: Solo Números", 61, 13, str(products['precio']))
            print("\n\033[94m\033[1mModificación del Stock:")
            print("\033[94m\033[1mIngrese el nuevo stock (Deje vacío para mantener el mismo): ")
            new_stock = validar.solo_decimales_and_espacios("Error: Solo Números", 61, 15, str(products['stock']))

            products["descripcion"] = new_nombre
            products["precio"] = new_precio
            products["stock"] = new_stock

            dato[producto_index] = products
            json_file.save(dato)
            print("\033[92mProducto actualizado exitosamente.")
            time.sleep(2)
        else:
            print(f"\nNo se encontró el producto con el ID: {producto_id}")
            time.sleep(1)
                
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        print("\033[95m" + "*" * 80)
        print("\033[95m*"*2 + " "*34 + "\033[1mEliminar un Producto" + " "*35 + "\033[95m*"*2)
        print("\033[95m" + "*" * 80)

        print("\033[1mIngrese nombre del producto:")
        gotoxy(2, 5)
        producto = validar.solo_letras("Error: Solo Letras", 30, 4).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        products = json_file.find("descripcion", producto)

        if products:
            product = products[0]
            print("\033[92m\033[1mID:\t\tDescripción:\t\tPrecio:\t\tStock:")
            print(f"\033[1m{product['id']}\t\t{product['descripcion']}\t\t${product['precio']}\t\t{product['stock']}")
            time.sleep(2)
            dato.remove(product)
            print("\033[91mProducto", product["descripcion"], "eliminado")
            time.sleep(2)
        else:
            print(f"\033[91mNo se encontró el producto con el nombre: {producto}")
            time.sleep(1)
        json_file.save(dato)

    def consult(self):
        validar = Valida()
        print('\033c', end='')
        print("\033[95m" + "*" * 80)
        print("\033[95m*"*2 + " "*32 + "\033[1mConsulta del Producto" + " "*33 + "\033[95m*"*2)
        print("\033[95m" + "*" * 80)

        print("\n\033[1mIngrese nombre del producto:")
        gotoxy(2, 6)  # Ajuste aquí para alinear correctamente con la presentación del título
        producto = validar.solo_letras("Error: Solo Letras", 30, 5).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("descripcion", producto)
        
        if products:
            product = products[0]
            print("\n\033[92m\033[1mID:\t\tDescripción:\t\tPrecio:\t\tStock:")
            print(f"\033[1m{product['id']:<13} {product['descripcion']:<23} ${product['precio']:<16} {product['stock']}\n")
            print("\033[95m" + "*" * 80)
            time.sleep(3)
        else:
            print(f"\n\033[91mNo se encontró el Producto con el nombre: {producto}")
            time.sleep(1)

class CrudSales(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = validar.solo_letras("Error: Solo Letras",53,9+line).lower()
        if procesar == "s" or procesar == "si":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)       
    
    def update(self):
        validar = Valida()
        sale = Sale
        print('\033c', end='')
        gotoxy(2, 1); print('\033[1;36m' + "█"*90)
        gotoxy(2, 2); print('\033[1;36m' + "██" + " "*34 + "Actualización de Factura" + " "*35 + "██")
        print("Ingrese el número de factura a actualizar: ")
        gotoxy(2, 4); invoice_number = validar.solo_numeros("Error: Solo Numeros", 44, 3)
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1); print('\033[1;36m' + "█"*90)
        gotoxy(2, 2); print('\033[1;36m' + "██" + " "*34 + "Actualización de Factura" + " "*35 + "██")
        if invoice_number.isdigit():
            invoice_number = int(invoice_number)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    invoice_found = True
                    gotoxy(2, 5); print(f"-"*109)
                    gotoxy(48, 5); print('\033[1;35m' + f"Impresion de la Factura # {invoice_number}" + '\033[0m')
                    gotoxy(5, 6); print('\033[1;33m' + "Factura" + '\033[0m')
                    gotoxy(8, 7); print(f"{invoice_number}")
                    gotoxy(18, 6); print('\033[1;33m' + "Fecha" + '\033[0m')
                    gotoxy(16, 7); print(f"{invoice['Fecha']}")
                    gotoxy(33, 6); print('\033[1;33m' + "Cliente" + '\033[0m')
                    gotoxy(31, 7); print(f"{invoice['cliente']}")
                    gotoxy(48, 6); print('\033[1;33m' + "Subtotal" + '\033[0m')
                    gotoxy(50, 7); print(f"{invoice['subtotal']}")
                    gotoxy(64, 6); print('\033[1;33m' + "Descuento" + '\033[0m')
                    gotoxy(67, 7); print(f"{invoice['descuento']}")
                    gotoxy(80, 6); print('\033[1;33m' + "IVA" + '\033[0m')
                    gotoxy(80, 7); print(f"{invoice['iva']}")
                    gotoxy(91, 6); print('\033[1;33m' + "Total" + '\033[0m')
                    gotoxy(91, 7); print(f"{invoice['total']}")
                    gotoxy(2, 9); print("-"*109)
                    gotoxy(48, 9); print('\033[1;35m' + "Impresion de los Detalles" + '\033[0m')
                    linea_x = 2
                    linea_y = 11
                    for idx, detalle in enumerate(invoice['detalle'], 1):
                        gotoxy(linea_x, linea_y)
                        print('\033[1;36m' + f"Detalle {idx}:" + '\033[0m')
                        gotoxy(linea_x, linea_y + 1)
                        print('\033[1;37m' + f"Producto: {detalle['poducto']}" + '\033[0m')
                        gotoxy(linea_x, linea_y + 2)
                        print('\033[1;37m' + f"Precio: {detalle['precio']}" + '\033[0m')
                        gotoxy(linea_x, linea_y + 3)
                        print('\033[1;37m' + f"Cantidad: {detalle['cantidad']}" + '\033[0m')
                        linea_x += 25
                    gotoxy(2, 16); print("-"*109)
                    gotoxy(2, 18);input("Presione Enter para seguir...")
                    borrarPantalla()
                    print('\033c', end='')
                    gotoxy(2, 1); print('\033[1;37m' + "█"*90)
                    gotoxy(2, 2); print('\033[1;37m' + "██" + " "*34 + "Actualización de Factura" + " "*35 + "██")
                    print('\033[0m' + "¿Qué desea actualizar?")
                    print('\033[0m' + "1. Fecha")
                    print('\033[0m' + "2. Cliente")
                    print('\033[0m' + "3. Subtotal")
                    print('\033[0m' + "4. Descuento")
                    print('\033[0m' + "5. Iva")
                    print('\033[0m' + "6. Total")
                    print('\033[0m' + "7. Detalle (Agregar/Actualizar/Eliminar)")
                    print('\033[0m' + "8. Cancelar")
                    gotoxy(1, 13); print('\033[0m' + 'Seleccione una opcion:', end="")
                    gotoxy(1, 13); opcion = validar.solo_numeros("Error: Solo numeros", 24, 13)

                    if opcion == '1':
                        print('\033[1;37m' + "Ingrese la nueva fecha (YYYY-MM-DD): " + '\033[0m')
                        nueva_fecha = validar.solo_fecha("Error: Solo Formato de Fecha", 39, 14)
                        invoice["Fecha"] = nueva_fecha
                    elif opcion == '2':
                        gotoxy(2, 14); print('\033[1;37m' + "Ingrese el nuevo cliente: " + '\033[0m')
                        gotoxy(2, 2); nuevo_cliente = validar.solo_letras("Error: Solo letras", 28, 14).lower().capitalize()
                        invoice["cliente"] = nuevo_cliente
                    elif opcion == '3':
                        gotoxy(2, 14); print('\033[1;37m' + "Ingrese el nuevo subtotal: " + '\033[0m')
                        gotoxy(2, 14); nuevo_subtotal = validar.solo_decimales("Error: Solo numeros", 28, 14) 
                        invoice["14ubtotal"] = float(nuevo_subtotal)
                    elif opcion == '4':
                        gotoxy(2, 14); print('\033[1;37m' + "Ingrese el nuevo descuento: " + '\033[0m')
                        gotoxy(2, 14); nuevo_descuento = validar.solo_decimales("Error: Solo numeros", 28, 14) 
                        invoice["14escuento"] = float(nuevo_descuento)
                    elif opcion == '5':
                        gotoxy(2, 14); print('\033[1;37m' + "Ingrese el nuevo IVA: " + '\033[0m')
                        gotoxy(2, 14); nuevo_iva = validar.solo_decimales("Error: Solo numeros", 28, 14) 
                        invoice["iva"] = float(nuevo_iva)
                    elif opcion == '6':
                        gotoxy(2, 14); print('\033[1;37m' + "Ingrese el nuevo total: " + '\033[0m')
                        gotoxy(2, 14); nuevo_total = validar.solo_decimales("Error: Solo numeros", 28, 14)
                        invoice["total"] = float(nuevo_total)
                    elif opcion == '7':
                        subopcion = input("¿Qué desea hacer en el detalle? ( 1)agregar / 2)actualizar / 3)eliminar): ")
                        borrarPantalla()
                        print('\033c', end='')
                        gotoxy(2, 1); print('\033[1;37m' + "█"*90)
                        gotoxy(2, 2); print('\033[1;37m' + "██" + " "*34 + "Actualización de Factura" + " "*35 + "██")
 
                        if subopcion == '1':
                            # Agregar nuevo producto al detalle
                            print('\033[0m' + "Ingrese el nombre del producto: ")
                            producto_nuevo = validar.solo_letras("Error: Solo Letras",33,3).lower().capitalize()
                            json_file1 = JsonFile(path+'/archivos/products.json')
                            product_vali = json_file1.find("descripcion",producto_nuevo)
                            if not product_vali:
                                print("producto no existe")
                                time.sleep(1)
                                return
                            product_vali = product_vali[0]
                            precio_nuevo = product_vali["precio"]
                            gotoxy(2,4);print(f'Precio del producto:{precio_nuevo}')
                            #print('\033[0m' + "Ingrese el precio del producto: ")
                            #precio_nuevo = validar.solo_decimales("Error: Solo Numeros",33,4)
                            print('\033[0m' + "Ingrese la cantidad del producto: ")
                            cantidad_nueva = validar.solo_numeros("Error: Solo Numeros",35,5)
                            nuevo_detalle = {"poducto": producto_nuevo, "precio": precio_nuevo, "cantidad": int(cantidad_nueva)}
                            invoice["detalle"].append(nuevo_detalle)
                            subtotal, discount, iva, total = sale.cal(invoice["detalle"], invoice["cliente"])
                            invoice["subtotal"] = round(subtotal, 2)
                            invoice["descuento"] = round(discount, 2)
                            invoice["iva"] = round(iva, 2)
                            invoice["total"] = round(total, 2)
                            print('\033[0m' + "Producto agregado al detalle.")
                            json_file.save(invoices)
                            break
                        
                        elif subopcion == '2':
                            # Mostrar detalle actual y permitir actualizar precio o cantidad
                            print('\033[0m' + "Qué producto quiere actualizar (Ingrese el nombre): ")
                            subopcion_update = validar.solo_letras("Error: Solo Letras",54,3).lower().capitalize()
                            invoice["detalle"]
                            for product in invoice["detalle"]:
                                if product["poducto"] == subopcion_update:
                                    print('\033[0m' + "ok, ingresa los nuevos datos:\n")
                                    print('\033[0m' + 'Ingresa el nuevo nombre:')
                                    product_new = validar.solo_letras("Error: Solo letras",26,6).lower().capitalize()
                                    json_file2 = JsonFile(path+'/archivos/products.json')
                                    product_vali = json_file2.find("descripcion",product_new)
                                    if not product_vali:
                                        print("producto no existe")
                                        time.sleep(1)
                                        return
                                    product_vali = product_vali[0]
                                    product["poducto"] = product_new
                                    product["precio"] = product_vali["precio"]
                                    gotoxy(2,6);print('\033[0m' + f"Precio del producto: {product["precio"]}")
                                    print('\033[0m' + 'Ingresa la nueva cantidad:')
                                    product["cantidad"] = validar.solo_numeros("Error: Solo Numeros",29,7)
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"],invoice["cliente"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                    json_file.save(invoices)
                            else:
                                print('\033[0m' + "Producto no encontrado en la factura")
                                time.sleep(1)

                            
                        elif subopcion == '3':
                            if len(invoice["detalle"]) == 1:
                                print('\033[0m' + "Solo queda un producto. Si elimina el ultimo producto, se le borrara automaticamente toda la factura")
                                print('\033[0m' + "¿Desea eliminar el producto? (s/n):")
                                opcion_eliminar_factura = validar.solo_letras("Error: Solo Letras",39,4)
                                if opcion_eliminar_factura.lower() == "s" or opcion_eliminar_factura.lower() == "si":
                                    invoices.remove(invoice)
                                    json_file.save(invoices)
                                    print('\033[0m' + "Factura eliminada.")
                                    break
                                else:
                                    print('\033[0m' + "Eliminacion de Factura Cancelada...")
                                    break

                            # Mostrar detalle actual y permitir eliminar un producto
                            print('\033[0m' + 'Qué producto quiere eliminar (Ingrese el nombre): ')
                            subopcion_update = validar.solo_letras("Error: Solo letras",51,3).lower().capitalize()
                            for i, product in enumerate(invoice["detalle"]):
                                if product["poducto"] == subopcion_update:
                                    del invoice["detalle"][i]
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"],invoice["cliente"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                    print('\033[0m' + "Producto eliminado.")
                                    json_file.save(invoices)
                                    break
                            else:
                                print('\033[0m' + "Producto no encontrado.")

                        else:
                            print("Opción no válida.")
                            break
                    elif opcion == '8':
                        print("Operación de actualización cancelada.")
                        break
                    else:
                        print("Opción no válida.")
                        break
                    
                    json_file.save(invoices)
                    break

            if not invoice_found:
                print(f"No se encontró la factura con el número {invoice_number}.")
        else:
            print("Por favor, ingrese un número de factura válido.")

        input("Presione una tecla para continuar...")
        
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color + "█"*90)
        gotoxy(2,2);print(purple_color + "██" + " "*34 + ("Eliminación de Factura") + " "*35 + "██")
        gotoxy(2,4);print(purple_color + "Ingrese el número de factura a eliminar: ")
        gotoxy(2,4);invoice_number = validar.solo_numeros("Error: Solo Numeros",44,4)
        invoice_num = int(invoice_number)
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        busqueda = json_file.find("factura",invoice_num)
        if busqueda:
            invoice = busqueda[0]
            print(white_color + f"Impresion de la Factura#{invoice_num}")
            gotoxy(13,6);print(purple_color + "----------------------------- Factura Encontrada ---------------------------")
            gotoxy(13,7);print(purple_color + "Factura    ")
            gotoxy(26,7);print(purple_color + "Fecha      ")
            gotoxy(39,7);print(purple_color + "Cliente    ")
            gotoxy(52,7);print(purple_color + "Subtotal   ")
            gotoxy(65,7);print(purple_color + "Descuento  ")
            gotoxy(78,7);print(purple_color + "IVA        ")
            gotoxy(91,7);print(purple_color + "Total  ")
            gotoxy(13,8);print(white_color + f"{invoice['factura']}         ")
            gotoxy(26,8);print(white_color + f"{invoice['Fecha']}¦¦")
            gotoxy(39,8);print(white_color + f"{invoice['cliente']}        ")
            gotoxy(52,8);print(white_color + f"{invoice['subtotal']}      ")
            gotoxy(65,8);print(white_color + f"{invoice['descuento']}      ")
            gotoxy(78,8);print(white_color + f"{invoice['iva']}      ")
            gotoxy(91,8);print(white_color + f"{invoice['total']}      ")

            gotoxy(13,9);print(purple_color + "---------------------------------- Detalles -------------------------------")
            detalles=invoice["detalle"]
            gotoxy(13,11);print(purple_color + "Producto   ")
            gotoxy(26,11);print(purple_color + "Precio     ")
            gotoxy(39,11);print(purple_color + "Cantidad   ")
            linea=0
            for detail in detalles:
                gotoxy(13,12+linea);print(white_color + detail["poducto"])
                gotoxy(26,12+linea);print(white_color + str(detail["precio"]))
                gotoxy(39,12+linea);print(white_color + str(detail["cantidad"]))
                linea+=1
            gotoxy(13,13+linea);print("-"*70)   
            gotoxy(13,14+linea);print("¿Seguro que deseas eliminar esta factura (si/no)?: ")
            confirmacion = validar.solo_letras("Error: Solo Letras",64,14+linea).lower()
            if confirmacion == 'si' or confirmacion == "s":
                invoices.remove(invoice)
                json_file.save(invoices)
                print("Factura eliminada exitosamente.")
                time.sleep(1)
            else:
                print("Operación de eliminación cancelada.")
                time.sleep(1)
        else:
            print(f"No se encontró la factura con el número {invoice_number}.")
            time.sleep(1)
    
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color + "█"*90)
        gotoxy(2,2);print("██" + " "*34 + "\033[1m\033[34mConsulta de Venta\033[0m" + " "*35 + "██")
        gotoxy(2,4);invoice= input("Ingrese el Numero de la Factura  ").strip()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(purple_color + "█"*90)
        gotoxy(2,2);print("██" + " "*34 + "\033[1m\033[34mConsulta de Venta\033[0m" + " "*35 + "██")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            gotoxy(1,5);print("-"*109)
            gotoxy(38, 5);print("\033[1m\033[36mImpresion de la Factura # {}\033[0m".format(invoice))
            if invoices:
                factura_info = invoices[0]
                gotoxy(2, 7); print("\033[1m\033[32mFactura\033[0m")
                gotoxy(15, 7); print("\033[1m\033[32mFecha\033[0m")
                gotoxy(30, 7); print("\033[1m\033[32mCliente\033[0m")
                gotoxy(45, 7); print("\033[1m\033[32mSubtotal\033[0m")
                gotoxy(60, 7); print("\033[1m\033[32mDescuento\033[0m")
                gotoxy(75, 7); print("\033[1m\033[32mIVA\033[0m")
                gotoxy(90, 7); print("\033[1m\033[32mTotal\033[0m")
                gotoxy(5, 8); print(f"{factura_info['factura']}")
                gotoxy(13, 8); print(f"{factura_info['Fecha']}")
                gotoxy(28, 8); print(f"{factura_info['cliente']}")
                gotoxy(46, 8); print(f"{factura_info['subtotal']}")
                gotoxy(62, 8); print(f"{factura_info['descuento']}")
                gotoxy(75, 8); print(f"{factura_info['iva']}")
                gotoxy(90, 8); print(f"{factura_info['total']}")
                gotoxy(1,10);print("-"*109)
                gotoxy(38, 10);print("\033[1m\033[35mImpresion de los detalles\033[0m")
                detalles = factura_info['detalle']
                linea_x = 2
                linea_y = 12
                for idx, detalle in enumerate(detalles, 1):
                    gotoxy(linea_x, linea_y)
                    print("\033[1m\033[35mDetalle {}:\033[0m".format(idx))
                    gotoxy(linea_x, linea_y + 1)
                    print(f"Producto: {detalle['poducto']}")
                    gotoxy(linea_x, linea_y + 2)
                    print(f"Precio: {detalle['precio']}")
                    gotoxy(linea_x, linea_y + 3)
                    print(f"Cantidad: {detalle['cantidad']}")
                    linea_x += 25
                gotoxy(1,17);print("-"*109)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("\033[1m\033[35mConsulta de Facturas\033[0m")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), invoices, 0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        gotoxy(2,40);x=input("presione una tecla para continuar...")
                
            

def ConsultasGenerales():
    borrarPantalla()
    
    # PRODUCTO CON MÁS STOCK
    json_file = JsonFile(path+'/archivos/products.json') 
    # se lee el json productos
    products = json_file.read() 
    # se crea un list comprehension con 2 for, el primero usará enumerate 
    # para identificar el index de los productos con mayor stock
    # el segundo for se usa para encontrar la mayor cantidad de stock de algún producto
    # entonces se hace una validación para únicamente guardar los productos que
    # tengan la mayor cantidad de stock (se guardan los diccionarios de cada producto del json products)
    products_major_stock = [products[idx] for idx, stock in enumerate(products) if stock["stock"] == max([x['stock'] for x in products])]
    print("\033[1;32m**"*50)
    gotoxy(40,2);print("PRODUCTO CON MAYOR STOCK") 
    gotoxy(13,4);print("Producto   ")
    gotoxy(26,4);print("Precio     ")
    gotoxy(39,4);print("Stock   ")
    linea=0
    for x in products_major_stock:
        gotoxy(13,6+linea);print(x["descripcion"])
        gotoxy(26,6+linea);print(x["precio"])
        gotoxy(39,6+linea);print(x["stock"])
        linea+=1
    print("*"*100)    
    
    # PRODUCTO CON MENOS STOCK
    # básicamente es lo mismo de arriba pero en el segundo for se guarda la menor cantidad de stock
    products_menor_stock = [products[idx] for idx, stock in enumerate(products) if stock["stock"] == min([x['stock'] for x in products])]
    print("\033[1;35m*****"*20)
    gotoxy(40,8+linea);print("PRODUCTO CON MENOR STOCK")
    gotoxy(13,10+linea);print("Producto   ")
    gotoxy(26,10+linea);print("Precio     ")
    gotoxy(39,10+linea);print("Stock   ")
    for x in products_menor_stock:
        gotoxy(13,12+linea);print(x["descripcion"])
        gotoxy(26,12+linea);print(x["precio"])
        gotoxy(39,12+linea);print(x["stock"])
        linea+=1
    print("*****"*20)    
    
    # CLIENTES CON MÁS FACTURAS
    # se identifican y se leen los json de facturas y clientes
    json_file_invoices = JsonFile(path+'/archivos/invoices.json')
    json_file_clients = JsonFile(path+'/archivos/clients.json')
    invoices = json_file_invoices.read()
    
    # se crea un set/conjunto con el dni de todos los clientes de las facturas
    clients = set([x['dni'] for x in invoices]) 
    
    # se crea un list comprehension que tendrá diccionarios
    # se realiza un ciclo for de los dni y los guardamos en un diccionario
    # también se guarda el número de facturas que existen con ese dni, usando el .find de los json
    dicionary_clients = [{'dni': client, 'facturas': len(json_file_invoices.find('dni', client))} for client in clients] 
    
    # se crea un list comprehension usando la misma lógica que se usó para obtener los
    # productos con mayor y menor stock. El primer for recorrerá los diccionarios de todos los clientes 
    # el segundo for usará la función max() para encontrar la cantidad máxima de facturas
    # luego usando una validación, se guardan los diccionarios de los clientes que tengan la mayor
    # cantidad de facturas.
    clients_invoices = [x for x in dicionary_clients if x['facturas'] == max([x['facturas'] for x in dicionary_clients])]

    # se valida si existe más de un elemento en la lista clients_invoices
    # se usará el .find de los json para buscar a los clientes en el json de clientes
    # si se encuentra el dni, lo presenta.
    # si existe más de 1 elemento en la lista, se hará lo mismo pero realizando un ciclo for
    print("\033[1;33m**"*50)
    gotoxy(40,14+linea);print("CLIENTES CON MÁS FACTURAS")
    if len(clients_invoices) == 1:
        client_found = json_file_clients.find('dni', clients_invoices[0]['dni'])
        gotoxy(13,16+linea);print("DNI   ")
        gotoxy(26,16+linea);print("Nombre     ")
        gotoxy(39,16+linea);print("Apellido   ")
        gotoxy(52,16+linea);print("Numero de Facturas")
        if client_found:
            for x in client_found:
                gotoxy(13,18+linea);print(x["dni"])
                gotoxy(26,18+linea);print(x["nombre"])
                gotoxy(39,18+linea);print(x["apellido"])
                gotoxy(52,18+linea);print(clients_invoices[0]['facturas'])
                linea+=1
    elif len(clients_invoices) > 1 :
        gotoxy(13,16+linea);print("DNI   ")
        gotoxy(26,16+linea);print("Nombre     ")
        gotoxy(39,16+linea);print("Apellido   ")
        gotoxy(52,16+linea);print("Numero de Facturas")
        for x in clients_invoices:
            client_found = json_file_clients.find('dni', x['dni'])
            if client_found:
                for x in client_found:
                    gotoxy(13,18+linea);print(x["dni"])
                    gotoxy(26,18+linea);print(x["nombre"])
                    gotoxy(39,18+linea);print(x["apellido"])
                    gotoxy(52,18+linea);print(clients_invoices[0]['facturas'])
                linea+=1
    print("**"*50)
    
    # FACTURAS CON MAYOR VALOR
    invoices_higher_value = [x for x in invoices if x['total'] == max([x['total'] for x in invoices])]
    print("\033[1;32m**"*50)
    gotoxy(40, 20+linea);print("FACTURAS CON MAYOR VALOR")
    if invoices_higher_value: 
        gotoxy(2, 22+linea); print("Factura")
        gotoxy(15,22+linea); print("Fecha")
        gotoxy(30,22+linea); print("Cliente")
        gotoxy(45,22+linea); print("Subtotal")
        gotoxy(60,22+linea); print("Descuento")
        gotoxy(75, 22+linea); print("IVA")
        gotoxy(90,22+linea); print("Total")
        for x ,f in enumerate(invoices_higher_value):
            factura_info = invoices_higher_value[x]
            gotoxy(5, 24+linea); print(f"{factura_info['factura']}")
            gotoxy(13, 24+linea); print(f"{factura_info['Fecha']}")
            gotoxy(28, 24+linea); print(f"{factura_info['cliente']}")
            gotoxy(46, 24+linea); print(f"{factura_info['subtotal']}")
            gotoxy(62, 24+linea); print(f"{factura_info['descuento']}")
            gotoxy(75, 24+linea); print(f"{factura_info['iva']}")
            gotoxy(90, 24+linea); print(f"{factura_info['total']}")
            linea+=1
    print("**"*50)
    
    
    # FACTURAS CON MENOR VALOR
    invoices_lower_value = [x for x in invoices if x['total'] == min([x['total'] for x in invoices])]
    print("\033[1;35m**"*50)
    gotoxy(40, 27+linea);print("FACTURAS CON MENOR VALOR")
    if invoices_lower_value: 
        gotoxy(2, 29+linea); print("Factura")
        gotoxy(15,29+linea); print("Fecha")
        gotoxy(30,29+linea); print("Cliente")
        gotoxy(45,29+linea); print("Subtotal")
        gotoxy(60,29+linea); print("Descuento")
        gotoxy(75, 29+linea); print("IVA")
        gotoxy(90,29+linea); print("Total")
        for x ,f in enumerate(invoices_lower_value):
            factura_info = invoices_lower_value[x]
            gotoxy(5, 31+linea); print(f"{factura_info['factura']}")
            gotoxy(13, 31+linea); print(f"{factura_info['Fecha']}")
            gotoxy(28, 31+linea); print(f"{factura_info['cliente']}")
            gotoxy(46, 31+linea); print(f"{factura_info['subtotal']}")
            gotoxy(62, 31+linea); print(f"{factura_info['descuento']}")
            gotoxy(75, 31+linea); print(f"{factura_info['iva']}")
            gotoxy(90, 31+linea); print(f"{factura_info['total']}")
            linea+=1
    print("**"*50)

opc=''
while opc !='5':
    borrarPantalla()
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Consultas Generales", "5) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            clients = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
            elif opc1 == "5":
                print("Regresando al menu Clientes...")
            # time.sleep(2)
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()
            products = CrudProducts()
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                products.update()
            elif opc2 == "3":
                products.delete()
            elif opc2 == "4":
                products.consult()
            elif opc2 == "5":
                print("Regresando al menu Clientes...")
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                time.sleep(2)
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
            elif opc3 == "5":
                print("Regresando al menu Clientes...")
    elif opc == "4":
        ConsultasGenerales()
        input("Presione una tecla para salir...")

    print("Regresando al menu Principal...")
    
    # time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()