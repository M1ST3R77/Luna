.. _Database:

Contents of Luna's interaction database
=======================================

.. code-block:: json

    {
        "intents": [
            {
                "tag": "non_reconnu",
                "patterns": [],
                "responses": ["Désolé, je ne comprends pas cette commande.", "Pouvez-vous reformuler s'il vous plaît ?"],
                "action": null
            },
            {
                "tag": "salutations",
                "patterns": ["Salut", "Bonjour", "Coucou", "Hey", "Hello"],
                "responses": ["Salut !", "Bonjour, comment puis-je vous aider ?", "Bonjour, en quoi puis-je être utile aujourd'hui ?", "Hey, ravi de vous voir !"],
                "action": null
            },
            {
                "tag": "remerciements",
                "patterns": ["Merci", "beaucoup", "aide", "gentil"],
                "responses": ["Avec plaisir !", "Je suis là pour vous aider !", "Pas de souci !", "C'est un plaisir de vous aider !"],
                "action": null
            },
            {
                "tag": "au_revoir",
                "patterns": ["revoir", "Bye", "bientôt", "y aller", "Adieu"],
                "responses": ["Au revoir !", "À bientôt !", "Bonne journée et à bientôt !", "Prenez soin de vous !"],
                "action": null
            },
            {
                "tag": "update",
                "patterns": ["mets", "jour", "mise", "jour", "update", "maj"],
                "responses": ["La mise à jour est en cours..."],
                "action": "update"
            },
            {
                "tag": "option",
                "patterns": ["switch", "options", "change d'options", "change d'option", "option", "debug", "normal", "Debug", "Normal"],
                "responses": ["L'option est en cours de changement..."],
                "action": "switch_option"
            },
            {
                "tag": "stop",
                "patterns": ["Arrêt", "Arrête-toi", "Arrête", "toi", "Stop", "Stop-toi"],
                "responses": ["Arrêt de Luna, Bonne journée !"],
                "action": "stop"
            },
            {
                "tag": "break",
                "patterns": ["Pause", "Repos", "Repose toi", "Repose-toi"],
                "responses": ["Luna est en pause, appuyée sur '²' pour la relancer."],
                "action": "break_opt"
            },
            {
                "tag": "mode",
                "patterns": ["switch", "mode", "change de mode", "vocal", "vocale", "input", "Vocal", "Input"],
                "responses": ["Le mode est en cours de changement..."],
                "action": "switch_mode"
            },
            {
                "tag": "audio",
                "patterns": ["active", "désactive", "l'audio", "audio"],
                "responses": ["L'audio est en cours de changement..."],
                "action": "switch_audio"
            },
            {
                "tag": "date",
                "patterns": ["date", "donne", "quel", "jour"],
                "responses": ["La date d'aujourd'hui est..."],
                "action": "get_date"
            },
            {
                "tag": "hours",
                "patterns": ["heure", "donne", "quel", "l'heure"],
                "responses": ["Il est actuellement..."],
                "action": "get_hours"
            },
            {
                "tag": "weather",
                "patterns": ["le temps", "donne", "quel", "météo"],
                "responses": ["La météo actuelle..."],
                "action": "get_weather"
            },
            {
                "tag": "search",
                "patterns": ["lancement", "lance", "recherche"],
                "responses": ["Que souhaitez-vous rechercher :"],
                "action": "search"
            },
            {
                "tag": "launch_exec",
                "patterns": ["lancement", "lance", "démarre", "démarrage", "exécutables", "exécutable", "applications", "application", "appli"],
                "responses": ["Que souhaitez-vous utiliser :"],
                "action": "launch_exec"
            },
            {
                "tag": "audio_gender",
                "patterns": ["switch", "voix", "change de voix", "femme", "homme"],
                "responses": ["Le changement de voix est en cours..."],
                "action": "switch_voice"
            }
        ]
    }