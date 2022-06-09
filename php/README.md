# Carre

![Logo du Carré](carre-logo.png)


Carré est un système de fichiers en temps-réel servant de plateforme à la collaboration et au regroupement d'information.

Carré est codé en Python ( et PHP par le passé), HTML5+CSS3 et Javascript.

## Fonctionnalitées

Carré est utilisé par navigateur, et affiche une hiérarchie de documents en temps-réel, comme Etherpad ou Hedgedocs. Cette hiérarchie est composée de dossier et de fichiers.

Il intègre également un système d'utilisateurices, permmettant de restraindre la création, suppression, réorganisation et affichage des documents. Il permet aussi l'accès et l'édition anonyme.

Il possède également un système de thèmes, permettant d'être rapidement adapté.

## Installation

Carré est pensé pour être installé sur un serveur Linux, et utilisé avec un proxy web inverse, tel que Nginx.

La procédure complète d'installation est décrire dans [Installation.md](). Rapidement ;

`git clone https://git.laquadrature.net/lqdn/carre.git`

`cd carre`

Éditez le fichier `config.json`, et remplissez les valeurs suivantes :

```
pad_server = "https://exemple.com"
```

avec l'adresse de votre serveur de pad.

Puis, faites ;

`nohup ./run.sh > carre.log`

Carré se lancera un serveur web sur l'adresse http://localhost:3553 .

Par défaut, Carré n'a pas d'utilisateurices. Vous pouvez en ajouter en créant un fichier `users.json`. Au lancement, Carré créera les utilisateurices trouvé dans ce fichier, et supprimera le fichier. Voir [Configuration.md]() pour toutes les options de configuration.

## Usage

<!-- Des photos d'illustration seraient les bienvenues -->

Une fois installé, carré commencera par afficher une hiérarchie vide, et une page d'aide.


Vous pouvez commencer à ajouter des fichiers ou des dossiers en cliquant une le symbole "+", ou en faisant un clique-droit.

Vous pouvez réorganiser la place des fichiers en les glissants.

Vous pouvez faire des suppressions en faisant un clique droit, ou bien en faisant une sélection et en appuyant sur la touche "Suppr" ou "Fn"+"⌫ Arrière"

Vous pouvez aussi effectuer des modifications directement dans le fichier `filesystem.json`.

## Développement

Toute aide est la bienvenue ! Pour le moment, le but est de garder le code et les fonctionnalitées aussi simples que possible. Il serait donc bienvenue d'avoir des retours, afin de simplifier encore les usages que l'on peut avoir de ce service.

Si vous avez des propositions, n'hésitez pas à le faire savoir, par mail ou en ouvrant un ticket.

## Crédits

La première version du carré, et l'inspiration pour la création de cette version à été faite par Oncela . Vous pouvez voir cette version dans la branche `archive` du dépôt git.

## Licence

```
 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
