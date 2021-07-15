# WhatsApp desktop:
Este complemento ha sido desarrollado para facilitar el uso de la aplicación agregando atajos de teclado para algunas funciones importantes, así como etiquetando algunos botones que no cuentan con nombre alguno.

## Instrucciones y comandos:
Al abrir WhatsApp desktop automáticamente va a activarse el modo foco. Pulsando shift tabulador luego de que termine de cargar la aplicación, colocará el foco en la lista de chats que podremos recorrer con flechas arriba y abajo.  
nota: Este complemento solo funciona con el modo foco activo.

### Atajos del complemento:

* Traer al frente la ventana de WhatsApp; Sin atajo asignado. Puede agregarse desde el diálogo gestos de entrada en la categoría Whatsapp. 
* Iniciar y enviar la grabación de un mensaje de voz; control + r.
* Iniciar y finalizar una llamada de voz al contacto del chat con el foco; alt + control + l.
* Iniciar y finalizar una llamada de video al contacto del chat con el foco; alt + control + v.
* Conocer el tiempo que lleva grabado el mensaje de voz; control + t.
* Copiar el texto del mensaje con el foco; control + shift + c.
* Abrir el link del mensaje con el foco en el navegador por defecto; control + l.
* Abrir el menú adjuntar; control + shift + a.
* Abrir el menú del chat; control + m.
* Abrir el menú general de WhatsApp; control + g.
* Reproducir el video en el mensaje con el foco; control + shift + v.
* Reproducir los mensajes de voz enfocando la barra de progreso; intro.
* Conocer el tiempo que lleva reproducido el mensaje de voz; control + t.
* Verbalizar el nombre del chat actual; control + shift + t.
* Descargar el archivo del mensaje cuando el mismo contiene alguno; alt + intro.
* Mover el foco al mensaje respondido. alt + control + intro.
* Retroceder 5 mensajes en la lista; control + flecha arriba.
* Avanzar 5 mensajes en la lista; control + flecha abajo.
* Conocer el estado del último mensaje enviado en el chat con el foco; control + shift + e.

### Atajos del modo edición:

* marcar y desmarcar el mensaje con el foco; barra espaciadora.
* Verbalizar el número de mensajes seleccionados; s.
* Reenviar los mensajes seleccionados; r.
* Eliminar los mensajes seleccionados; suprimir.
* Destacar los mensajes seleccionados; d.
* Salir del modo de selección; q.

### Visualización virtual de chats:
Esta funcionalidad es experimental, por lo que puede que sea removida en futuras actualizaciones del complemento.  
Su función principal es cargar y navegar entre una lista de chats de forma virtual para poder moverse entre ellos sin marcar los nuevos mensajes como leídos.  
Lamentablemente la aplicación no tiene una gestión lógica para las conversaciones, por lo que no existe un órden consonante de navegación. Y solo serán mostrados los chats visibles en la pantalla en el momento de refrescar la lista.  
Los atajos de esta funcionalidad son los siguientes:

* shift + f5: Refresca la lista de chats.
* shift + flecha arriba; verbaliza el chat anterior.
* shift + flecha abajo; verbaliza el chat siguiente.
* shift intro; enfoca el chat verbalizado

### Atajos generales de la aplicación:

* Crear nuevo chat; control + n.
* Activar el cuadro de búsqueda de chats; control + f.
* Archivar un chat; control + e.
* Menú contextual del chat; flecha derecha.
* Enfocar el chat siguiente; control + tabulador.
* Enfocar el chat anterior; control + shift + tabulador.
* Borrar el chat; control + shift + d.
* Fijar, desfijar chat; control + shift + p.
* Abrir el menú contextual del mensaje; flecha derecha
* Activar la búsqueda de mensajes del chat; control + shift + f.

## Instrucciones del modo de selección:
Para activar el modo de selección tendremos que activar el menú contextual  del mensaje con el foco, ya sea con el atajo control + m, o con la tecla aplicaciones.  
Una vez abierto el menú nos desplazamos con flechas abajo hasta la opción seleccionar mensajes, la cual debemos activar con intro.  
Al pulsar esta opción va a activarse una ventana que va a ser quitada automáticamente por el complemento para volver a enfocar la lista de mensajes, proceso que puede demorarse unos segundos. Si esto no sucede podemos probar con el atajo alt flecha derecha, o tabulando hasta al lista de mensajes.    
Si todo ha salido bien ya deberíamos estar en el modo de selección, lo que podremos corroborar pulsando la letra s que verbaliza los mensajes seleccionados.  
Una vez aquí podremos seleccionar y desseleccionar mensajes con la barra espaciadora, y una vez finalizada la selección podremos realizar las acciones siguientes:

* Eliminar los mensajes con la tecla suprimir.
* Reenviar los mensajes con la letra r.
* Destacar los mensajes con la letra d.
* Cerrar el modo de selección con la letra q.

Dependiendo de la función seleccionada va a activarse la ventana correspondiente. La de selección de contactos en el caso del reenvío, la ventana de confirmación en el caso de eliminación de mensajes, etc.
 
## Traducciones:
Las siguientes personas han colaborado traduciendo el complemento:
	Mustafa Elçiçek, al turco.  
	Rémy Ruiz, al francés.  
	Ângelo Miguel Abrantes, al portugués.
	
## Registro de cambios:  
### 0.8:

* Modificaciones generales para compatibilidad con la nueva versión de la app.
* Agregada función experimental de visualización virtual de chats.

### 0.7:

* Agregado atajo para reproducir el video de un mensaje.
* Agregados atajos para moverse por un número mayor de mensajes.
* Agregado modo de selección.
* Agregada función para conocer el estado del último mensaje enviado.
* Añadidos atajos para realizar llamadas de voz y de video. (Solo disponible para la versión Store)
* Añadida traducción al francés.

### 0.6:

* Añadida función para verbalizar el tiempo que lleva grabado un mensaje de voz.
* Simplificación de el proceso de reenvío de un mensaje.
* Correciones menores para compatibilizar los cambios de la aplicación.

### 0.5;

* Función añadida para leer el título del chat. El atajo es control + shift + t.
* Al reproducir un mensaje de voz con intro el foco se mueve a la barra de progreso, desde donde podremos adelantar o retroceder el mensaje con flechas derecha o izquierda.
* Función añadida para verbalizar el tiempo que lleva reproducido el mensaje desde la barra de progreso del mismo. El atajo es; control + t.
* Agregadas las líneas para traductores desde el español.

### 0.4;

* Agregada función global para traer al frente la ventana de whatsapp desde cualquier lugar.

### 0.3;
* Modificaciones en la documentación.