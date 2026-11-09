# QR Code Generator

Petite application de bureau pour générer un QR code à partir d'un lien ou d'un
texte, **entièrement en local** : aucune connexion réseau, aucune donnée envoyée
ailleurs.

Interface [Tkinter](https://docs.python.org/3/library/tkinter.html) (thème sombre),
encodage via la bibliothèque [`qrcodegen`](https://www.nayuki.io/page/qr-code-generator-library)
de Nayuki, rendu de l'image avec [Pillow](https://python-pillow.org/).

## Fonctionnalités

- Saisie d'un lien ou d'un texte, génération par un bouton ou la touche Entrée.
- Choix du **niveau de correction d'erreur** (Low / Medium / Quartile / High).
- Aperçu du QR code et affichage de la version et de la taille en modules.
- **Export PNG** haute résolution.
- Fonctionne hors-ligne, sans compte ni service tiers.

## Installation

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate   |   Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
python qrcode_app.py
```

## Remarques

L'encodage du QR code (standard, niveaux de correction compris) est fourni par la
bibliothèque `qrcodegen`. Ce projet est l'**application** autour : interface,
choix du niveau de correction, rendu de l'image et export PNG.

## Licence

[MIT](LICENSE) © 2026 Dorian Cession.
