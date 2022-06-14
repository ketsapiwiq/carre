# Carre

> 📄 Un système de classement de pad, basé sur une hiérarchie de fichiers, écrit en Javascript et Python

## ✍️ Usage

Carré s'utilise depuis un navigateur web, comme un gestionnaire de fichiers.

## 🔧 Installation

1 - Récupérer le code

`$ git clone gitlab@git.laquadrature.net:Oncela5eva/carre.git`

`$ cd carre`

### 💻 Développement

Pour faire votre développement, il vous suffit d'éxécuter le fichier `install.sh`. Il installe les dépendances via `pip`, et il va également lancer un serveur Flask.

> ⚠️ Par défaut, Carré utilise le serveur de pad de La Quadrature du Net. Merci de définir une autre URL quand vous faites vos tests et l'éventuelle mise en production. Des services de pad sont disponibles ici : [entraide.chatons.org](https://entraide.chatons.org)


### ⬛ Production

Pour la mise en production, vous aurez besoin de suivre [les instructions relative à la mise en production d'un serveur Flask](https://flask.palletsprojects.com/en/2.1.x/tutorial/deploy/). 

Vous aurez également besoin de modifier le fichier `config.ini`.

> ⚠️ Par défaut, Carré utilise le serveur de pad de La Quadrature du Net. Merci de définir une autre URL quand vous faites vos tests et l'éventuelle mise en production. Des services de pad sont disponibles ici : [entraide.chatons.org](https://entraide.chatons.org)


### ⬇️ Mises à jour

Pour mettre à jour votre installation, vous devrez :

- Faire une sauvegarde des fichiers suivants :
	- `config.ini`
	- `data/menuTreelib.json`
	- `src/users.db`
- Éxecuter les commandes suivante :
	- `git fetch origin`
		- Récupérer toutes les références des modifications
	- `git checkout 0.0.2` 
		- Appliquer les modifications pour la version 0.0.2
- La mise à jour est faite, vous pouvez relancer votre serveur

## 🧑‍💻 Développement

Toute aide est la bienvenue ! Pour le moment, le but est de garder le code et les fonctionnalitées aussi simples que possible. Il serait donc bienvenue d'avoir des retours, afin de simplifier encore les usages que l'on peut avoir de ce service.

Si vous avez des propositions, n'hésitez pas à le faire savoir, par mail ou en ouvrant un ticket.

### 📦 Organisation du code source

Le carré est construit autour des fichiers suivants ;

- src/ - Dossier contenant le code source en Python
- data/ - Dossier avec les données du menu
- static/ - Dossier avec les fichiers pour l'interface web
- config.ini - Le fichier de configuration
- README.md - Ce fichier
- install.sh - Le script bash qui permet de lancer l'installation et le serveur de développement 

## 🎖️ Licence

```
 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2022 Oncela <am@laquadrature.net>, Nono <np@laquadrature.net>, Erolf

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
```
