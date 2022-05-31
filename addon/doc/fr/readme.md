# WhatsApp desktop:
Cette extension a été développée pour faciliter l'utilisation de l'application en ajoutant des raccourcis clavier pour certaines fonctions importantes, ainsi que étiquetant quelques boutons qui n'ont aucun nom.

## Instructions et commandes clavier:
Lorsque vous ouvrez  WhatsApp desktop il s'activera automatiquement le Mode formulaire. En appuyant sur maj tab Après avoir terminé le chargement de l'application, il mettra le focus sur la liste des conversations que nous pouvons parcourir avec les flèches haut et bas.  
Remarque: cette extension ne fonctionne que avec le mode formulaire actif.

### Raccourcis de l'extension:

* Amener en avant-plan la fenêtre de WhatsApp; Sans raccourci  attribué. Il peut être ajouté à partir  du dialogue Gestes de commande dans la catégorie Whatsapp. 
* Ouvrir WhatsApp; Sans raccourci  attribué. Il peut être ajouté à partir  du dialogue Gestes de commande dans la catégorie Whatsapp. 
* Démarrer et envoyer l'enregistrement d'un message vocal; contrôle + r.
* Démarrer et terminer un appel vocal pour le contact de la conversation focalisé; alt + contrôle + l.
* Démarrer et terminer un appel vidéo pour le contact de la conversation focalisé; alt + contrôle + v.
* Connaître le temps que le message vocal a été enregistré; contrôle + t.
* Copier le texte du message focalisé; contrôle + maj + c.
* Ouvrir le lien du message focalisé dans le navigateur par défaut; contrôle + l.
* Ouvrir le menu joindre; contrôle + maj + a.
* Ouvrir le menu de conversation; contrôle + m.
* Ouvrir le menu principal de WhatsApp; contrôle + g.
* Lire la vidéo du message focalisé; contrôle + maj + v.
* Lire les messages vocaux focalisant la barre de progression; entrée.
* Basculer entre les vitesses de lecture d'un message vocal; barre d'espace.
* Connaître le temps que le message vocal a été lu; contrôle + t.
* Verbaliser le nom de la conversation en cours;; contrôle + maj + t.
* Télécharger le fichier du message quand il contient un; alt + entrée.
* Déplacer le focus vers le message répondu. alt + contrôle + entrée.
* Reculer 5 messages dans la liste; page précédente.
* Avancer 5 messages dans la liste; page suivante.
* Verbaliser le message en fonction de ça position; alt + 1 à 9 du clavier alphanumérique (Seulement à partir du dialogue d'édition de message).
* Basculer le focus entre la liste des messages et la zone d'édition lorsque vous entrez dans une cconversation; alt + flèche gauche.
* Appuyer sur le bouton Lire plus dans les messages texte; alt + flèche bas.
* Activar y desactivar la eliminación de los números de teléfono en los mensajes de contactos no agendados; control + shift +r

### Raccourcis généraux de l'application:

* Créer un nouveau chat; contrôle + n.
* Activer la zone de recherche dans la liste des chats; contrôle + f.
* Archiver la conversation; contrôle + e.
* Menu contextuel du chat; flèche droite.
* Mettre le focus sur le chat suivant; contrôle + tab.
* Mettre le focus sur le chat précédent; contrôle + maj + tab.
* Supprimer le chat; contrôle + maj + d.
* Épingler / Dépingler le chat; contrôle + maj + p.
* Ouvrir le menu contextuel du message; flèche droite.
* Activer la recherche de messages dans le chat; contrôle + maj + f.

### Raccourcis du mode de sélection:

* Cocher et décocher le message focalisé; barre d'espace.
* Verbaliser le nombre de messages sélectionnés; s.
* Renvoyer les messages sélectionnés; r.
* Supprimer les messages sélectionnés; effacement.
* Mettre en surbrillance les messages sélectionnés;; d.
* Quitter le mode de sélection; q.

## Canal de mise à jour:
À partir de la version 0.9 Un canal de mise à jour a été ajouté qui est désactivé par défaut.  
Pour l'activer, nous devons procéder comme suit:

* Ouvrir et focaliser la fenêtre WhatsApp.
* Affichez le menu NVDA avec le raccourci NVDA + n, puis aller dans Préférences, Paramètres.
* Recherchez WhatsApp dans la liste et tabuler afin de rechercher la case à cocher.
* Une fois cochée, Appliquer et OK afin de sauvegarder les changements

Chaque fois que nous démarrons WhatsApp avec cette fonctionnalité activée, l'extension comparera la version de l'extension du manifeste avec celle du dernier lancement du projet dans GitHub. S'il n'y a pas de coïncidences, une fenêtre est lancée laquelle vous permettra de télécharger et d'installer la nouvelle version.

## Instructions du mode de sélection:
Pour activer le mode de sélection, nous devrons activer le menu contextuel du message focalisé, soit avec le raccourci contrôle + m, ou avec la touche Applications.  
Une fois que le menu est ouvert, nous nous déplaçons avec les flèches base dans l'option Sélectionner les messages, que nous devons activer avec Entrée.  
En appuyant sur cette option elle permet d'activer une fenêtre qui sera automatiquement fermée par l'extension pour remettre le focus sur la liste des messages, processus qui peut prendre quelques secondes. Si cela ne se produit pas, nous pouvons essayer le raccourci alt flèche droit, ou en appuyant sur tab jusqu'à la liste des messages.  
Si tout c'est bien passé, nous devrions déjà être au mode de sélection, ce que nous pouvons corroborer en appuyant sur la lettre s qui verbalise les messages sélectionnés.  
Une fois ici, nous pouvons sélectionner et désélectionner des messages avec la barre d'espace et une fois la sélection terminée, nous pouvons effectuer les actions suivantes:

* Supprimer les messages avec la touche effacement.
* Renvoyer les messages avec la lettre r.
* Mettre en surbrillance les messages avec la lettre d.
* Fermer le mode de sélection avec la lettre q.

## Interfaz virtual de chats

En ciertas ocasiones los cambios introducidos en actualizaciones de la aplicación, rompen la correcta navegación con el foco del sistema entre la lista de chats.
Para estos casos he agregado una virtualización de los objetos de conversación. Esto  nos permite navegar entre la lista de chats que se muestran en la ventana, generalmente 19. Sin embargo el órden de los mismos suele ser bastante arbitrario, lo que el órden no es siempre el correcto en la lista virtualizada. 
Para activar esta virtualización tan solo hay que activar el cuadro de búsqueda de chats con el atajo control + "f". Al abrirse este cuadro, el complemento captura los objetos y los coloca en la lista virtual, la cual puede ser utilizada con los siguientes comandos:

* control + flecha arriba; verbaliza el chat anterior en la lista virtual.
* control + flecha abajo; verbaliza el chat siguiente en la lista virtual.
* control + shift + inicio; verbaliza el primer chat en la lista virtual.
* control + intro; mueve el foco al chat actual de la lista virtual.

Para acceder al chat de una lista, primero debemos  navegar con los atajos control + flechas arriba o abajo, enfocarla con control + intro, y luego pulsar solamente intro.

## Traductions:

	Les personnes suivantes ont collaboré à la traduction de l'extension:

	* Mustafa Elçiçek, pour le  turc.  
	* Rémy Ruiz, pour le français.  
	* Ângelo Miguel Abrantes, pour le portugais.  
	* Carlos Esteban Martínez Macías (anglais)
	* Valentin Kupriyanov (russe)
	* Michele Barbi (italien)
