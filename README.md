# Cliente_APISIAR
Este repositorio incluirá distintas funciones en código Python para explotar y extraer información de la v2 de la API del SIAR.
Para su uso es necesario tener en cuenta lo indicado en el manual de la API situado en: https://www.larioja.org/larioja-client/cm/agricultura/images?idMmedia=1499039

Incluye las funciones:

extrae_datos_climaticos_API(estacion, frecuencia, **filtros)
>Obtiene la respuesta de la apisiar. Si es correcta devuelve los datos (según la descripción del objeto de respuesta descritos en manual de la API)   
>>Si es incorrecta puede ser por tres razones:   
            - La API responde OK pero hay exceso de parámetros en la respuesta !!! PENDIENTE DE AÑADIR RECURSIVIDAD si count > nº máx registros  
            - La API responde OK pero hay algún otro error   
            - Error de comunicación con la API
  
genera_url_datosClimaticos(estacion, frecuencia, **filtros)
>Es una función auxiliar de extrae_datos_climaticos_API

filtra_datos_validos(response, incluir_datos_Sospechosos = False, valor_por_defecto_si_no_valido = "")
> A partir de un objeto respuesta como el generado en una respuesta válida de la API función extrae_datos_climaticos_API()
> permite extraer los datos válidos, da la opción de devolver los datos sospechosos y cambiar el valor que se sobreescribe si el dato no es válido
