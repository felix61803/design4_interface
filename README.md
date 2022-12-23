# Projet de design 4 - Système d'acquisition de données 

par :
- Félix Côté
- Albert bourdage
- Maxime Carpentier

étudiants en Génie Électrique à l'université Laval


## Specifications
- Le répertoire comprends des fichiers qui doivent être installé sur une Raspberry pi modèle 4B ainsi que des fichiers qui doivent être installés sur un ordinateur sur windows 10 ou 11 ayant git et python d'installé

## Procédure pour cloner le repertoire sur la Raspberry pi
détail de la procédure de clonage ici... <br>

ou le liens vers la documentation[ICI](./module_CAN/CanRead.py)

## Procédure pour cloner le repertoire sur l'ordinateur

 1) Assurez-vous que l'ordinateur utilise Windows 10 ou 11. Pour vérifier cette information. Aller dans paramètre. Sélectionnez Système et allez dans la section À propos.

 2) Assurez-vous que Git est installé sur l'ordinateur. Ouvrez un terminal (invite de commande ou cmd) et tapez cette commande :

        git --version

    
    Si git est installé, vous verrez quelque chose comme :

        git version 2.23.0.windows.1

3) Assurez-vous que Python 3 est installé sur l'ordinateur (avec l'option ADD TO PATH). Si vous ne savez pas si python 3 est déjà installé ou non, vous pouvez taper cette commande dans le terminal :

        python --version

    Si python est installé, vous verrez quelque chose comme :

        Python 3.9.7

4) Ouvrir un terminal et selectionner l'emplacement dans lequel vous desirer installer le répertoire en tappant dans le terminal:

        cd dossier1\sousdossier1\sousousdossier\...\emplacement

5) Tapper ensuite les commandes suivantes:

        git clone 
    
    suivi d'un espace et du lien HTTPS du répertoire (dans la section CODE en vert). Par exemple:

        git clone https://github.com/userx/Design_4.git

6) La documentation pour l'interface graphique se trouve dans le dossier interface_graphique\Machine_demo\manuel_utilisation. . 

- Vous pouvez l'ouvir en cliquant [ICI](./interface_graphique/Machine_demo/manuel_utilisation.pdf)

6) La documentation pour l'installation du calculateur modifié se trouve dans le dossier: importation_datas_calculateur\manuel_utilisation.pdf. 

- Vous pouvez l'ouvir en cliquant [ICI](./importation_datas_calculateur/manuel_utilisation.pdf)