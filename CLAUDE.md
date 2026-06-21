# BlindStack — Guide codebase pour Claude

## Contexte du projet

Jeu de cartes (variante type Blind) en Python/Django avec une interface CLI (typer + questionary). Pas de frontend web. Django est utilisé uniquement pour l'ORM, les migrations, et l'interface admin.

**Stack :** Django 6, SQLite, typer, questionary, django-ninja (installé mais non câblé), django-object-actions (actions dans l'admin), ruff (linter).

---

## Paradigme QuerySet — règle centrale

**Ne jamais créer de Manager personnalisé.** Toujours utiliser `QuerySet.as_manager()`.

**Règle :** toute opération sur un groupe d'instances → méthode sur le QuerySet. L'instance du modèle appelle ensuite cette méthode QuerySet pour les opérations sur elle-même.

```python
# QuerySet : opère sur une collection
class CardQuerySet(QuerySet):
    def generate_cards_of_game_round(self, game_round: "GameRound") -> Self:
        ...

# Modèle : délègue au QuerySet
class GameRound(Model):
    def add_cards(self) -> Self:
        Card.objects.generate_cards_of_game_round(game_round=self)
        return self
```

Les méthodes QuerySet retournent `Self` pour le chaînage. Les méthodes d'instance du modèle retournent aussi `Self`.

---

## Structure des fichiers

```
blind_stack_app/
  models/
    __init__.py        ← réexporte tous les modèles
    card.py
    card_value.py
    game_round.py
    participant.py
    player.py
    bot.py
    stack.py
  querysets/
    __init__.py        ← réexporte tous les QuerySets
    card.py
    card_value.py
    stack.py
    bot.py
cli_client/
  application.py      ← boucle principale CLI
  select_bots.py
  select_player.py
  start_new_game_round.py
```

Un modèle = un fichier. Un QuerySet = un fichier. Chaque `__init__.py` réexporte tout.

---

## Modèles

### Hiérarchie des participants

`Player` (humain, lié à `django.contrib.auth.User` via OneToOne) et `Bot` (with `is_unlocked`) sont les entités joueurs. Ils ne participent jamais directement à une `GameRound`.

`Participant` est le modèle pivot obligatoire. Il contient soit un FK vers `Player`, soit vers `Bot` — jamais les deux (contrainte XOR en base).

`GameRound` a 3 FK obligatoires vers `Participant` (`participant_1`, `participant_2`, `participant_3`) et 1 FK optionnel (`participant_4`).

**Pour accéder aux joueurs actifs d'une partie :** `game_round.active_participants` (property, retourne `list[Participant]`).

### Contraintes en base

Toujours utiliser `Meta.constraints` avec `CheckConstraint` et `UniqueConstraint` — pas uniquement des validators Python. Les contraintes Python (validators) s'ajoutent **en plus** pour les min/max numériques.

### Constantes min/max

Les limites numériques sont définies au niveau module ET répercutées sur la classe :

```python
CARD_VALUE_MIN: int = 1
CARD_VALUE_MAX: int = 12

class CardValue(Model):
    CARD_VALUE_MIN: int = CARD_VALUE_MIN
    CARD_VALUE_MAX: int = CARD_VALUE_MAX
```

### Imports circulaires

Utiliser `TYPE_CHECKING` + string annotations pour les références croisées entre modèles :

```python
from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    from blind_stack_app.models import GameRound
```

Les imports réels (ex. `from blind_stack_app.models.card import Card`) se font à l'intérieur des méthodes quand nécessaire pour éviter les cycles.

---

## Règles de style

- **Ruff** : line-length 150, double quotes, indent 4 espaces, target py311.
- Les migrations sont exclues du linter.
- Les `__init__.py` sont exemptés du tri d'imports (`I001`).
- Pas de commentaires sauf si le "pourquoi" est non-évident.

---

## État actuel — où en est le projet

### Ce qui fonctionne
- Tous les modèles sont en place et migrés (migration 0009 = dernière).
- L'admin Django permet de créer des `CardValue`, `Player`, `Bot`, `Participant`, `GameRound`, et d'y déclencher les actions de jeu (add_cards, add_stacks, shuffle_cards, distribute_cards).
- La sélection du joueur et des bots dans le CLI fonctionne.

### Ce qui est cassé / en cours

**1. Bug dans `CardQuerySet.distribute_cards`** (`blind_stack_app/querysets/card.py:32`) :
référence `game_round.active_players` qui n'existe plus depuis le refactor vers `Participant`. Doit être `game_round.active_participants`.

**2. `cli_client/start_new_game_round.py` est obsolète** :
utilise encore l'ancienne API `player_1=`, `player_2=`… Ces champs n'existent plus. Il faut maintenant créer des `Participant` puis passer `participant_1=`, `participant_2=`, `participant_3=`.

**3. Flux de jeu CLI commenté** (`cli_client/application.py:44-48`) :
```python
# TODO: reprendre ici
# game_round: GameRound = cli_start_new_game_round(player=player, bots=bots)
# game_round.add_cards()
# ...
```
Le prochain chantier est de débloquer ce flux après avoir corrigé les deux points ci-dessus.

---

## Mécanique du jeu (règles déduites du code)

- **24 cartes** : 2 couleurs (Black, White) × 12 valeurs (1–12).
- **6 piles** (stacks, rang 1–6) par partie.
- **3 à 4 participants** : toujours 1 `Player` humain + 3 `Bot` (depuis le CLI — le 4e participant est optionnel en modèle mais la sélection CLI force exactement 3 bots).
- Flux de jeu : créer la partie → `add_cards()` → `add_stacks()` → `shuffle_cards()` → `distribute_cards()`.