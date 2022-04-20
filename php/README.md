# Carre

> Un système de classement de pad, basé sur une hiérarchie de fichiers, écrit en Javascript et PHP

## Usage

Il suffit d'un serveur HTTP + PHP basique pour faire tourner ce service. Vous aurez aussi besoin d'une connexion vers un serveur Ehterpad pouvant créer des pads depuis n'importe quel URL.

## Installation

1 - Récupérer le code

`$ git clone gitlab@git.laquadrature.net:Oncela5eva/carre.git`
`$ cd carre`

2 - Créer un dossier "server" et donnez les droits au serveur ou à php d'écrire dedans.

`$ mkdir server`

2.1 - Pour faire du développement, vous pouvez utilisez PHP sur votre machine de développement avec la commande suivante ;

`$ php7 -S localhost:8080`

3 - Définir dans pad.js le début de l'URL des etherpad à créer/utiliser. Exemple :

`pad.adress = "https://pad.lqdn.fr/p/test_padwikirc";`

Merci de définir une autre URL quand vous faites vos tests et l'éventuelle mise en production. Des services de pad sont disponibles ici : [entraide.chatons.org](https://entraide.chatons.org)

4 - Facultatif : protéger l'accès au dossier "admin" via htaccess (pour protéger la modification du menu)

## Développement

Toute aide est la bienvenue ! Pour le moment, le but est de garder le code et les fonctionnalitées aussi simples que possible. Il serait donc bienvenue d'avoir des retours, afin de simplifier encore les usages que l'on peut avoir de ce service.

Si vous avez des propositions, n'hésitez pas à le faire savoir, par mail ou en ouvrant un ticket.

### Organisation du code source

Le carré est construit autour des fichiers suivants ;

- `index.html` contient la vue du client, et charge le code Javascript
	- `init.js` Initialise la page
	- `construct.js` construit le menu
  - `click.js` répond aux cliques de l'utilisateurice.
	- `option.js` actions modifiants le menu
	- `update.js` mise à jour du serveur
	- `pad.js` affiche les pages dans le pad
- `updateClient.php`
- `server/` va contenir les fichiers JSON décrivant l'état actuel du carré.
- `fonts/` contient les polices de caractères.
- `admin/` contient les fichiers PHP du serveur.
	- `updateServer.php` se charge de faire la mise à jour des fichiers du côté serveur en réponse aux requêtes des clients.

## Licence

```
 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Oncela <am@laquadrature.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
