# WhatsApp desktop:
Este complemento ha sido desarrollado para facilitar el uso de la aplicación agregando atajos de teclado para algunas funciones importantes, así como etiquetando algunos botones que no cuentan con nombre alguno.

## Instrucciones y comandos:
Al abrir WhatsApp desktop automáticamente va a activarse el modo foco. Pulsando shift tabulador luego de que termine de cargar la aplicación, colocará el foco en la lista de chats que podremos recorrer con flechas arriba y abajo.  
nota: Este complemento solo funciona con el modo foco activo.

### Atajos del complemento:

* Traer al frente la ventana de WhatsApp; Sin atajo asignado. Puede agregarse desde el diálogo gestos de entrada en la categoría Whatsapp. 
* Abrir WhatsApp; Sin atajo asignado. Puede agregarse desde el diálogo gestos de entrada en la categoría Whatsapp. 
* Iniciar y enviar la grabación de un mensaje de voz; control + r.
* Conmutar entre la lista de mensajes y el cuadro de edición; alt + flecha izquierda.
* Iniciar  una llamada de voz al contacto del chat con el foco; alt + control + l.
* Iniciar  una llamada de video al contacto del chat con el foco; alt + control + v.
* Conocer el tiempo que lleva grabado el mensaje de voz; control + t.
* Copiar el texto del mensaje con el foco; control + shift + c.
* Abrir el link del mensaje con el foco en el navegador por defecto; control + l.
* Abrir el menú adjuntar; control + shift + a.
* Abrir el menú del chat; control + m.
* Abrir el menú general de WhatsApp; control + g.
* Reproducir el video en el mensaje con el foco; control + shift + v.
* Reproducir los mensajes de voz enfocando la barra de progreso; intro.
* Conmutar entre las velocidades de reproducción de un mensaje de voz; barra espaciadora.
* Conocer el tiempo que lleva reproducido el mensaje de voz; control + t.
* Verbalizar el nombre del chat actual; control + shift + t.
* Descargar el archivo del mensaje cuando el mismo contiene alguno; alt + intro.
* Mover el foco al mensaje respondido. alt + control + intro.
* Retroceder 5 mensajes en la lista; retroceso página.
* Avanzar 5 mensajes en la lista; avance página.
* Verbalizar el mensaje según su posición; alt + 1 al 9 (Solo desde el cuadro de edición de mensaje).
* Pulsar el botón leer más en los mensajes de texto; alt + flecha abajo.

### Atajos generales de la aplicación:

* Crear nuevo chat; control + n.
* Activar el cuadro de búsqueda de chats; control + f.
* Archivar un chat; control + e.
* Menú contextual del chat; flecha derecha.
* Enfocar el chat siguiente; control + tabulador.
* Enfocar el chat anterior; control + shift + tabulador.
* Borrar el chat; control + shift + d.
* Fijar, desfijar chat; control + shift + p.
* Abrir el menú contextual del mensaje; flecha derecha.
* Activar la búsqueda de mensajes del chat; control + shift + f.

### Atajos del modo de selección:

* marcar y desmarcar el mensaje con el foco; barra espaciadora.
* Verbalizar el número de mensajes seleccionados; s.
* Reenviar los mensajes seleccionados; r.
* Eliminar los mensajes seleccionados; suprimir.
* Destacar los mensajes seleccionados; d.
* Salir del modo de selección; q.

## Canal de actualización:
A partir de la versión 0.9 se ha añadido un canal de actualización el cual viene desactivado por defecto.  
Para activarlo debemos realizar los siguientes pasos:

* abrir y enfocar la ventana de WhatsApp.
* Mostrar el menú de NVDA con el atajo NVDA + n, e ingresar en preferencias, opciones.
* Buscar WhatsApp en la lista y tabular para encontrar la casilla de verificación.
* Una vez marcada, aplicar y aceptar para guardar los cambios.

Cada vez que iniciemos WhatsApp con esta función activada, el complemento va a comparar la versión del complemento del manifiesto con el último lanzamiento del proyecto en github. Si no hay coincidencias se lanza  una ventana que permitirá descargar e instalar la nueva versión.

## Instrucciones del modo de selección:
Para activar el modo de selección tendremos que activar el menú contextual  del mensaje con el foco, ya sea con el atajo control + m, o con la tecla aplicaciones.  
Una vez abierto el menú nos desplazamos con flechas abajo hasta la opción seleccionar mensajes, la cual debemos activar con intro.  
Al pulsar esta opción va a activarse una nueva ventana. Para volver a enfocar la lista de mensajes hay que pulsar el atajo alt flecha derecha, o tabular hasta la lista de los mismos.  
Si todo ha salido bien ya deberíamos estar en el modo de selección, lo que podremos corroborar pulsando la letra s que verbaliza los mensajes seleccionados.  
Una vez aquí podremos seleccionar y desseleccionar mensajes con la barra espaciadora, y una vez finalizada la selección podremos realizar las acciones siguientes:

* Eliminar los mensajes con la tecla suprimir.
* Reenviar los mensajes con la letra r.
* Destacar los mensajes con la letra d.
* Cerrar el modo de selección con la letra q.

Dependiendo de la función seleccionada va a activarse la ventana correspondiente. La de selección de contactos en el caso del reenvío, la ventana de confirmación en el caso de eliminación de mensajes, etc.
 
## Traducciones:
Las siguientes personas han colaborado con las traducciones del complemento:  
	Mustafa Elçiçek (turco)
	Rémy Ruiz (francés)
	Ângelo Miguel Abrantes (portugués)
	Carlos Esteban Martínez Macías (inglés)
	* Valentin Kupriyanov (ruso)

## Registro de cambios:  
### 2.2149.4:

* Función añadida para pulsar el botón leer más en los mensajes de texto muy extensos.
* Mejoras en la función para copiar el texto del mensaje al portapapeles.
* La verbalización del nombre del chat ahora funciona desde la lista de conversaciones, y desde cualquier lugar dentro de la misma.

### 2.2142.12

* Modificaciones para compatibilidad con la versión 2.2142.12

### 2.2140.5

* Modificaciones para compatibilidad con la versión 2.2140.5
* Gesto agregado para conmutar entre la lista de mensajes y el cuadro de edición dentro de un chat.

### 2.2134.10

* Gesto agregado para conmutar entre la lista de mensajes y el cuadro de edición.
* Modificaciones para compatibilidad con la versión 2.2134.10

### 1.1:

* Modificaciones para compatibilidad con la versión 2.2130.9
* Eliminada la función experimental de lectura virtual de chats.
* Correcciones menores.

### 1.0:

* Lectura del historial de mensajes de un chat desde el cuadro de texto.
* Correcciones generales.

### 0.9:

* Añadido canal de actualización.
* Agregada función para modificar la velocidad de los mensajes de voz.
* Correcciones menores.

### 0.8:

* Modificaciones generales para compatibilidad con la nueva versión de la app.
* Agregada función experimental de visualización virtual de chats.

### 0.7:

* Agregado atajo para reproducir el video de un mensaje.
* Agregados atajos para moverse por un número mayor de mensajes.
* Agregado modo de selección.
* Agregada función para conocer el estado del último mensaje enviado.
* Añadidos atajos para realizar llamadas de voz y de video.
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