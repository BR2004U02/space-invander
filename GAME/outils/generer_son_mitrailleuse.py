"""Génère les bruitages de la compétence « mitrailleuse » (synthèse sonore, sans enregistrement).

Dépendance : numpy (pip install numpy). Le module wave fait partie de Python.

Lancement, depuis la racine du dépôt :
    python GAME/outils/generer_son_mitrailleuse.py
    python GAME/outils/generer_son_mitrailleuse.py --demo demo.wav   (séquence complète à écouter)

Quatre fichiers, calés sur l'affichage à 60 images par seconde :
    mitrailleuse_demarrage.wav  0,4 s = 24 images   le canon se met à tourner (animation d'ouverture)
    mitrailleuse_rotation.wav   0,5 s = 30 images   le canon tourne, à jouer en boucle (se referme sans clic)
    mitrailleuse_tir.wav        0,25 s              un coup de feu, à jouer à chaque balle (une toutes les 0,2 s)
    mitrailleuse_arret.wav      0,4 s = 24 images   le canon ralentit et s'arrête (animation de fermeture)
"""
import os
import sys
import wave

import numpy as np

SR = 44100                    # échantillons par seconde
FPS = 60
D_OUVERTURE = 24 / FPS        # 0,4 s
D_BOUCLE = 30 / FPS           # 0,5 s : durée de la boucle de rotation
D_CADENCE = 12 / FPS          # 0,2 s entre deux balles = 6 images de tir + 6 images de rotation
D_TIR = 0.25
PASSAGES_PAR_S = 10           # un canon passe devant toutes les 6 images, comme dans l'animation
F_MOTEUR_MIN, F_MOTEUR_MAX = 30, 120   # ronronnement du moteur, en Hz
COUPURE_MOTEUR = 1100                  # au-dessus de cette fréquence le moteur est étouffé : son plus sourd

rng = np.random.default_rng(43)


# ------------------------------------------------------------------ outils
def temps(duree):
    return np.arange(int(round(duree * SR))) / SR


def filtre(x, bas=None, haut=None, periodique=False):
    """Garde les fréquences entre bas et haut (Hz). periodique=True : le signal reste bouclable."""
    n = len(x)
    y = x if periodique else np.concatenate([x, np.zeros(2048)])
    spectre = np.fft.rfft(y)
    f = np.maximum(np.fft.rfftfreq(len(y), 1 / SR), 1e-6)
    gain = np.ones_like(f)
    if bas:
        gain *= 1 / np.sqrt(1 + (bas / f) ** 6)
    if haut:
        gain *= 1 / np.sqrt(1 + (f / haut) ** 6)
    return np.fft.irfft(spectre * gain, len(y))[:n]


def ajouter(tampon, son, position, boucle=False):
    """Mixe un petit son dans le tampon. boucle=True : ce qui dépasse la fin revient au début."""
    idx = position + np.arange(len(son))
    if boucle:
        np.add.at(tampon, idx % len(tampon), son)
    else:
        ok = idx < len(tampon)
        tampon[idx[ok]] += son[ok]


def lissage(t, duree):
    """Passe de 0 à 1 en douceur (départ et arrivée progressifs)."""
    x = np.clip(t / duree, 0, 1)
    return x * x * (3 - 2 * x)


def toc(amplitude):
    """Battement sourd et doux : un canon qui passe."""
    t = temps(0.06)
    attaque = np.clip(t / 0.003, 0, 1)                          # montée progressive : pas de claquement
    grave = np.sin(2 * np.pi * 260 * t) * np.exp(-t / 0.014)
    frottement = filtre(rng.standard_normal(len(t)), 150, 700) * np.exp(-t / 0.008)
    return amplitude * attaque * (0.8 * grave + 0.35 * frottement)


def clac(amplitude):
    """Verrou plus grave : la trappe."""
    t = temps(0.07)
    metal = np.sin(2 * np.pi * 420 * t) * np.exp(-t / 0.018) + 0.5 * np.sin(2 * np.pi * 1130 * t) * np.exp(-t / 0.010)
    choc = filtre(rng.standard_normal(len(t)), 300, 4000) * np.exp(-t / 0.006)
    return amplitude * (0.6 * metal + 0.6 * choc)


# ------------------------------------------------------------------ moteur
N_BOUCLE = int(round(D_BOUCLE * SR))
MARGE = int(0.1 * SR)         # 0,1 s à pleine vitesse ajoutée puis coupée : évite un clic aux raccords
SOUFFLE = filtre(rng.standard_normal(N_BOUCLE), 180, 800, periodique=True)   # souffle commun aux trois sons


def moteur(vitesse, boucle=False, avant=0, apres=0, depart_souffle=0):
    """Son du canon rotatif pour une courbe de vitesse (0 = arrêté, 1 = pleine vitesse).

    avant / apres : nombre d'échantillons à pleine vitesse ajoutés avant / après, puis retirés.
    depart_souffle : position dans le souffle commun, pour qu'il se prolonge d'un son à l'autre.
    """
    n = len(vitesse)
    v = np.concatenate([np.ones(avant), vitesse, np.ones(apres)])
    f = F_MOTEUR_MIN + (F_MOTEUR_MAX - F_MOTEUR_MIN) * v
    phase = 2 * np.pi * (np.cumsum(f) - f) / SR
    ronron = np.sin(phase) + 0.45 * np.sin(2 * phase) + 0.2 * np.sin(3 * phase) + 0.08 * np.sin(4 * phase)
    engrenage = 0.3 * np.sin(1.5 * phase) + 0.1 * np.sin(4.5 * phase)

    passages = (np.cumsum(PASSAGES_PAR_S * v) - PASSAGES_PAR_S * v) / SR      # canons déjà passés
    souffle = SOUFFLE[(depart_souffle - avant + np.arange(len(v))) % N_BOUCLE]
    souffle = souffle * (0.7 + 0.3 * np.cos(2 * np.pi * passages))            # pulse au rythme des canons

    son = v ** 0.6 * (0.42 * ronron + 0.25 * engrenage + 0.30 * v * souffle)

    if boucle:                                                  # un battement tous les 0,1 s
        positions = [int(round(k * SR / PASSAGES_PAR_S)) for k in range(int(round(n / SR * PASSAGES_PAR_S)))]
    else:                                                       # un battement à chaque canon qui passe
        positions = [0] + list(np.nonzero(np.diff(np.floor(passages + 1e-9)) > 0)[0] + 1)
    for pos in positions:
        if pos < len(v) - 1 or boucle:
            ajouter(son, toc(0.10 + 0.14 * v[min(pos, len(v) - 1)]), pos, boucle)

    son = filtre(son, haut=COUPURE_MOTEUR, periodique=boucle)   # étouffe les aigus
    return son[avant:avant + n]


def son_rotation():
    return moteur(np.ones(N_BOUCLE), boucle=True)


def son_demarrage():
    t = temps(D_OUVERTURE)
    son = moteur(lissage(t, D_OUVERTURE), apres=MARGE, depart_souffle=N_BOUCLE - len(t))
    ajouter(son, clac(0.4), 0)                                  # la trappe s'ouvre
    return son


def son_arret():
    t = temps(D_OUVERTURE)
    son = moteur(1 - lissage(t, D_OUVERTURE), avant=MARGE)
    ajouter(son, clac(0.45), int(0.33 * SR))                    # la trappe se referme (6 dernières images)
    return son


# ------------------------------------------------------------------ tir
def son_tir():
    t = temps(D_TIR)
    n = len(t)
    bruit = rng.standard_normal
    claquement = filtre(bruit(n), bas=2000) * np.exp(-t / 0.004)
    corps = filtre(bruit(n), 150, 2500) * np.exp(-t / 0.035)
    f_coup = 45 + 115 * np.exp(-t / 0.03)                       # 160 Hz qui descend vers 45 Hz
    coup = np.sin(2 * np.pi * np.cumsum(f_coup) / SR) * np.exp(-t / 0.05)
    echo = filtre(bruit(n), haut=1200) * np.exp(-t / 0.07)

    son = 1.0 * claquement + 0.9 * corps + 0.9 * coup + 0.25 * echo

    td = np.clip(t - 0.03, 0, None)                             # culasse
    culasse = (np.sin(2 * np.pi * 1830 * td) + 0.6 * np.sin(2 * np.pi * 2740 * td)
               + 0.4 * np.sin(2 * np.pi * 4120 * td)) * np.exp(-td / 0.02) * (t >= 0.03)
    son += 0.12 * culasse
    for depart, ampli in ((0.09, 0.045), (0.15, 0.025)):          # douille qui tombe et rebondit
        td = np.clip(t - depart, 0, None)
        son += ampli * (np.sin(2 * np.pi * 5200 * td) + 0.7 * np.sin(2 * np.pi * 7300 * td)) \
            * np.exp(-td / 0.03) * (t >= depart)

    son = np.tanh(1.6 * son)                                    # écrêtage doux : donne du punch
    fin = int(0.02 * SR)
    son[-fin:] *= np.linspace(1, 0, fin)
    return son


# ------------------------------------------------------------------ fichiers
def ecrire(chemin, son):
    pcm = np.clip(son, -1, 1)
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((pcm * 32767).astype("<i2").tobytes())


def fabriquer():
    rotation, demarrage, arret, tir = son_rotation(), son_demarrage(), son_arret(), son_tir()
    gain = 0.45 / np.max(np.abs(rotation))        # même gain pour les trois sons du moteur : pas de saut de volume
    return {
        "mitrailleuse_demarrage.wav": demarrage * gain,
        "mitrailleuse_rotation.wav": rotation * gain,
        "mitrailleuse_arret.wav": arret * gain,
        "mitrailleuse_tir.wav": tir * (0.95 / np.max(np.abs(tir))),
    }


def demo(sons, nb_tirs=15):
    """Séquence complète telle qu'elle sera jouée en jeu."""
    duree_tir = nb_tirs * D_CADENCE
    total = np.zeros(int(round((2 * D_OUVERTURE + duree_tir + 0.3) * SR)))
    debut = int(round(D_OUVERTURE * SR))
    fin = debut + int(round(duree_tir * SR))
    ajouter(total, sons["mitrailleuse_demarrage.wav"], 0)
    boucle = sons["mitrailleuse_rotation.wav"]
    for pos in range(debut, fin, len(boucle)):                  # la boucle tourne pendant tout le tir
        ajouter(total, boucle[:fin - pos], pos)
    for k in range(nb_tirs):
        ajouter(total, sons["mitrailleuse_tir.wav"], debut + int(round(k * D_CADENCE * SR)))
    ajouter(total, sons["mitrailleuse_arret.wav"], fin)
    return total * (0.95 / np.max(np.abs(total)))


if __name__ == "__main__":
    dossier = "GAME/assets/audio/sfx"
    sons = fabriquer()
    os.makedirs(dossier, exist_ok=True)
    for nom, son in sons.items():
        ecrire(os.path.join(dossier, nom), son)
        print(f"{nom:30s} {len(son) / SR:.2f} s = {len(son) / SR * FPS:.0f} images")
    if "--demo" in sys.argv:
        chemin = sys.argv[sys.argv.index("--demo") + 1]
        ecrire(chemin, demo(sons))
        print("démo :", chemin)
