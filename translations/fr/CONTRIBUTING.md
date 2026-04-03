<p align="center">
Traductions <br>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/de/CONTRIBUTING.md>🇩🇪 DE   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/CONTRIBUTING.md>🇬🇧 EN   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/fr/CONTRIBUTING.md>🇫🇷 FR   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/hu/CONTRIBUTING.md>🇭🇺 HU   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/hi/CONTRIBUTING.md>🇮🇳 HI   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/id/CONTRIBUTING.md>🇮🇩 ID   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/it/CONTRIBUTING.md>🇮🇹 IT   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/nl/CONTRIBUTING.md>🇳🇱 NL   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/pt-br/CONTRIBUTING.md>🇧🇷 PT-BR   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/ru/CONTRIBUTING.md>🇷🇺 RU   </a>
<a href="https://github.com/Ciphey/Ciphey/tree/master/translations/th/CONTRIBUTING.md">🇹🇭 TH   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/zh/CONTRIBUTING.md>🇨🇳 ZH   </a>
</p>

Salut !

Vous êtes donc intéressé à contribuer à Ciphey ? 🤔

Mais peut-être que vous vous inquiétez de savoir par où commencer, ou vous pensez que vos compétences en programmation ne sont pas "assez bonnes". Eh bien, ce dernier point - c'est ridicule ! Nous sommes parfaitement d'accord avec du "mauvais code", et de toute façon, si vous avez lu ce document, vous êtes probablement un excellent programmeur. Je veux dire, les débutants ne contribuent généralement pas aux projets GitHub 😉

Voici quelques façons dont vous pouvez contribuer à Ciphey :

- Le traduire dans une nouvelle langue 🧏
- Ajouter plus de formats de chiffrement 📚
- Créer plus de documentation (très important ‼️ nous en serions éternellement reconnaissants)
- Corriger les bugs dans les GitHub Issues (nous vous aiderons dans cette tâche 😊)
- Refactoriser la base de code 🥺

Si cela semble difficile, ne vous inquiétez pas ! Ce document explique exactement comment accomplir ces tâches. Et plus encore.... Votre nom sera ajouté à la liste des contributeurs de Ciphey, et nous en serions éternellement reconnaissants ! 🙏

Nous avons un petit serveur Discord où vous pouvez discuter avec les développeurs et obtenir de l'aide. Alternativement, rédigez une GitHub-Issue pour votre suggestion. Si vous souhaitez rejoindre Discord :

[Serveur Discord](https://discord.gg/KfyRUWw)

# Comment contribuer

Ciphey a toujours besoin de plus d'outils de décodage ! Si vous voulez savoir comment intégrer du code dans les chiffrements, regardez ceci :

- <https://github.com/Ciphey/Ciphey/wiki/Adding-your-own-ciphers> exemple simple
- <https://github.com/Ciphey/Ciphey/wiki/Extending-Ciphey> référence de l'API

Il serait bien si vous pouviez écrire quelques tests pour cela, il suffit de copier une fonction dans le fichier Ciphey/tests/test_main.py et remplacer le texte chiffré par quelque chose d'encodé avec votre chiffrement. Si vous n'ajoutez pas de tests, nous fusionnerons probablement quand même le code, mais diagnostiquer les bugs sera beaucoup plus difficile !

Il va sans dire que nous vous ajouterons à la liste des contributeurs pour votre travail acharné !

# Ajouter une nouvelle langue 🧏

Le vérificateur de langue par défaut, `brandon`, fonctionne avec de nombreuses langues. Cela peut paraître effrayant.
Mais honnêtement, tout ce que vous devez faire, c'est prendre un dictionnaire, faire un peu d'analyse (nous avons du code d'aide pour cela), puis ajouter le dictionnaire et l'analyse à un dépôt. Ensuite, vous ajoutez la langue au fichier `settings.yml`.

# Créer plus de documentation

La documentation est la partie la plus importante de Ciphey. Plus il y a de documentation, mieux c'est.

Et croyez-moi quand je dis que si vous contribuez à une excellente documentation, vous apparaîtrez au même niveau que les contributeurs de code. La documentation est essentielle.

Vous pouvez contribuer à la documentation de plusieurs façons.

- Ajouter des docstrings dans le code
- Améliorer la documentation actuelle (README, ce fichier, notre site Read The Docs)
- Traduire la documentation

Et bien plus encore !

# Corriger les bugs

Allez sur notre page GitHub-Issues où vous trouverez tous les problèmes de Ciphey ! Corrigez-les et vous serez ajouté à la liste des contributeurs ;)

# Refactoriser la base de code

Toutes les parties de Ciphey ne suivent pas les directives PEP8, et il y a beaucoup de code dupliqué.
