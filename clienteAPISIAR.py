"""
    Esta primera versión es una prueba de concepto para probar el funcionamiento de la API

    Existen distintas partes del código que necesitan revisión, están marcados con el símbolo !!!

"""
import requests

API_URL_ROOT = "https://ias1.larioja.org/apiSiar/servicios/v2/"

def genera_url_datosClimaticos(estacion, frecuencia, **filtros):
    """
    Es función auxiliar de extrae_datos_climaticos_API()

    La url a la que se envía la petición descarta los valores de filtros no válidos, no es necesario analizarlos por nuestra parte
    Ej de la variable filtros = {fecha_inicio: "2015-06-02", funcion = "Max"}, ver manual API los filtros aceptados
    """

    api_url = API_URL_ROOT + "datos-climaticos/" + str(estacion) + "/" + frecuencia # Creamos URL según manual API
    
    if len(filtros) > 0: # probar esta función sin esta condición, si len = 0 (la variable filtro no está definida / está vacía funciona?¿?¿?)
        char_union = "?" # Si hay un filtro se usa el caracter "?" para separar la sintaxis de la consulta principal de los filtros
        for key, value in filtros.items():
            api_url = api_url + char_union + key + "=" + value
            char_union = "&" # Después del primer filtro, si hay otros, se encadenan con "&"
    

    return(api_url)

# Test
#genera_url_datosClimaticos(501, "M")
#genera_url_datosClimaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"})


def extrae_datos_climaticos_API(estacion, frecuencia, **filtros):
    """
        Obtiene la respuesta de la apisiar. Si es correcta devuelve los datos (según la descripción del objeto de respuesta descritos en manual)
        Si es incorrecta puede ser por dos razones:
            - La API responde OK pero hay exceso de parámetros en la respuesta !!! PENDIENTE DE AÑADIR RECURSIVIDAD
            - La API responde OK pero hay algún otro error (???PUEDE SUCEDER???)
            - Error de comunicación con la API (!!!Pendiente gestionar excepción)

        Observaciones:

         !!!posible problema si el usuario quiere más de un parámetro y/o más de una función por cómo se usan los diccionarios y la sintaxis de la API
         !!! pendiente añadir alguna funcionalidad para debugging, si DEBUG = TRUE entonces devolver la api_url generada e información sobre la respuesta recibida.
   
    """
    api_url = genera_url_datosClimaticos(estacion, frecuencia, **filtros)

    res = requests.get(api_url) # conectamos con esa url método GET y guardamos el contenido en la variable res
    
    if res.ok:
        res = res.json() # lo que nos interesa de la respuesta está en el json, contiene variable count, "success" y "datos"
        if(res["success"] == 'true'): # ojo!!! res["success"]): # si ha funcionado
            if(int(res["count"]) > 0):
                return(res["datos"])
            else:
                print("Ningun dato disponible. str(res) = " + str(res))
        else:
            print("Error al recibir los datos. str(res) = " + str(res))
    else:
        print("Error al comunicar con la API")

# Test
#print("Extraer datos de la url = " + genera_url_datosClimaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"}))
#datos_clima = extrae_datos_climaticos_API(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"})



def filtra_datos_validos(response, incluir_datos_Sospechosos = False, valor_por_defecto_si_no_valido = ""):
    """
    Este es un primer borrador de esta función, modifica la salida para simplificarla, 
    la modificación está adaptada a los usos comunes de los datos extraidos
    desde la API
    !!! Probablemente lo que se debería hacer es un filtro que devolviera sólo los casos válidos, 
        pero con la misma estructura que lo que ofrece la API (estudiar pandas y los dfs por si se puede hacer en modo R, sin bucle for)
        Si la salida simplificada es útil se puede hacer depender la salida de una variable simplify = True/False
    """
    datos_validados = []
    #!!! si solo tiene un valor, da fallos, usar otra forma para gestionar el json
    if  isinstance(response, dict): # si solo tiene un registro, es un diccionario
        dato_valido = response["dato_valido"]
        
        if dato_valido == "V":
            valor = response["valor"]
        elif (incluir_datos_Sospechosos and dato_valido == "S"):
            valor = response["valor"]
        #elif (valor_por_defecto_si_no_valido != ""):
        #    valor = valor_por_defecto_si_no_valido
        else:
            valor = valor_por_defecto_si_no_valido
            
        datos_validados.append({"parametro": response["parametro"],
                                "funcion_agregacion": response["funcion_agregacion"],
                                "fecha": response["fecha"],
                                "valor": valor})
    else:
        for i in range(0, len(response)):
            dato_valido = response[i]["dato_valido"]
        
            if dato_valido == "V":
                valor = response[i]["valor"]
            elif (incluir_datos_Sospechosos and dato_valido == "S"):
                valor = response[i]["valor"]
            #elif (valor_por_defecto_si_no_valido != ""):
            #    valor = valor_por_defecto_si_no_valido
            else:
                valor = valor_por_defecto_si_no_valido
            
            datos_validados.append({"parametro": response[i]["parametro"],
                                "funcion_agregacion": response[i]["funcion_agregacion"],
                                "fecha": response[i]["fecha"],
                                "valor": valor})
    
    return(datos_validados)


# Test
#print("Extraer datos de la url = " + genera_url_datosClimaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "P", "funcion": "Ac"}))
#datos_brutos_lluvia = extrae_datos_climaticos_API(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "P", "funcion": "Ac"})
#datos_lluvia = filtra_datos_validos(datos_brutos_lluvia, incluir_datos_Sospechosos = False, valor_por_defecto_si_no_valido = "") 

             
def extrae_datos_parametro(datos_brutos, parametro):
    """
        Dada un objeto de salida con el formato de la apisiar o el formato simplificado tras función filtra_datos
        extrae del objeto aquellos registros cuyo parámetro sea el solicitado
    """
    datos_filtrados = []
    for i in range(0, len(datos_brutos)):
        if datos_brutos[i]["parametro"] == parametro:
            datos_filtrados.append(datos_brutos[i])
    
    return(datos_filtrados)

