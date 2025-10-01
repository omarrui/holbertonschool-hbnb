# HBnB Evolution – Technical Documentation (Part 1)

Cette documentation couvre la première partie du projet **HBnB Evolution**, qui consiste à créer une base technique solide pour l’application. L’objectif est de présenter l’architecture et les interactions entre les différentes couches du système.

## Diagrams

### 1. High-Level Package Diagram - PackageDiagram
Ce diagramme montre la structure générale de l’application, organisée en trois couches principales :
- **Presentation Layer** : services qui gèrent l’interaction avec l’utilisateur.  
- **Business Logic Layer** : modèles et logique métier (User, Place, Review, Amenity).  
- **Persistence Layer** : accès aux données et opérations sur la base de données.  

Les flèches indiquent le flux de communication entre les couches, avec le **facade pattern** utilisé pour simplifier les interactions.

### 2. Sequence Diagram – Review Submission
Ce diagramme illustre le processus par lequel un utilisateur soumet un avis pour un lieu :
1. L’utilisateur envoie sa requête via l’API.  
2. La couche Présentation (ReviewController) transmet la requête à la logique métier (ReviewService).  
3. La couche Persistence (ReviewRepository) sauvegarde l’avis dans la base de données.  
4. La confirmation remonte à l’utilisateur.  

Ce diagramme est cohérent avec la structure du package diagram, respectant le flux Présentation → Business Logic → Persistence.

### 3. Sequence Diagram – Fetching a List of Places - fetchPlacesSequence
Ce diagramme montre le processus par lequel un utilisateur récupère la liste des lieux :
1. L’utilisateur fait une requête via l’API (PlaceController).  
2. La logique métier (PlaceService) récupère les données depuis la base (PlaceRepository).  
3. Les résultats sont renvoyés à l’utilisateur.
