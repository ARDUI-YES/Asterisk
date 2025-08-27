### Configuration requise pour la service météorlogique en français (prononcer le degree en français)
## Loader le module channel
    Vérifiez que votre fichier /etc/asterisk/modules.conf contient une ligne :
    load => func_channel.so
    Puis faire : 
    sudo asterisk -r
    module load func_channel.so
    core show function CHANNEL
## Installer la langue fr pour pouvoir prononcer les digits en fr
  si il n'y a pas le dossier /var/lib/asterisk/sounds/fr dans votre pc, veuillez l'installer par la commande suivante
  
    ```sudo apt update```
    
    ```sudo apt install asterisk-core-sounds-fr-gsm```
Après installation le dossier fr se trouveras dans ​/usr/share/asterisk/sounds donc il faut créer un lien symbolique vers de fichier dans /var/lib/asterisk/sounds/

    ```sudo ln -s /usr/share/asterisk/sounds/fr /var/lib/asterisk/sounds/fr ```
