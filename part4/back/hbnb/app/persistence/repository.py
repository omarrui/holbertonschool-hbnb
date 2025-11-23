from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
# from app import db  # TEMP FIX: circular import


class Repository(ABC):
    @abstractmethod
    def add(self, obj: Any) -> None:
        """Ajoute un objet au dépôt."""
        raise NotImplementedError

    @abstractmethod
    def get(self, obj_id: str) -> Optional[Any]:
        """Récupère un objet par son id."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Récupère tous les objets."""
        raise NotImplementedError

    @abstractmethod
    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        """Met à jour un objet avec un dict de valeurs."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj_id: str) -> None:
        """Supprime un objet par son id."""
        raise NotImplementedError

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        """Récupère le premier objet dont l'attribut == valeur."""
        raise NotImplementedError


class InMemoryRepository(Repository):

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def add(self, obj: Any) -> None:
        self._data[obj.id] = obj

    def get(self, obj_id: str) -> Optional[Any]:
        return self._data.get(obj_id)

    def get_all(self) -> List[Any]:
        return list(self._data.values())

    def list(self) -> List[Any]:
        return self.get_all()

    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        obj = self.get(obj_id)
        if not obj:
            return None

        if hasattr(obj, "update") and callable(getattr(obj, "update")):
            obj.update(data)
        else:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            if hasattr(obj, "save") and callable(getattr(obj, "save")):
                obj.save()

        return obj

    def delete(self, obj_id: str) -> None:
        if obj_id in self._data:
            del self._data[obj_id]

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        for obj in self._data.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None


class SQLAlchemyRepository(Repository):
    """Repository implementation using SQLAlchemy ORM.
    """

    def __init__(self, model, db=None):
        self.model = model
        self.db = db or self._get_db()
    
    def _get_db(self):
        # Import db only when needed to avoid circular import
        from app import db
        return db

    def add(self, obj: Any) -> None:
        self.db.session.add(obj)
        self.db.session.commit()

    def get(self, obj_id: str) -> Optional[Any]:
        return self.model.query.get(obj_id)

    def get_all(self) -> List[Any]:
        return self.model.query.all()

    def update(self, obj_id: str, data: Dict[str, Any]) -> Optional[Any]:
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db.session.commit()
        return obj

    def delete(self, obj_id: str) -> None:
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        return self.model.query.filter_by(**{attr_name: attr_value}).first()