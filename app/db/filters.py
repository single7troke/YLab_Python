class Specification:
    def is_satisfied(self):
        raise NotImplementedError


class BaseFilter(Specification):
    def __init__(self, _id):
        self.id = _id

    def is_satisfied(self):
        pass


class GetSingleMenuFilter(BaseFilter):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id

    def is_satisfied(self):
        return {'id': self.id}


class GetSingleSubmenuFilter(BaseFilter):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id

    def is_satisfied(self):
        return {'id': self.id}


class GetSingleDishFilter(BaseFilter):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id

    def is_satisfied(self):
        return {'id': self.id}


class GetAllMenusFilter(Specification):
    def is_satisfied(self):
        return {}


class GetAllSubmenusFilter(BaseFilter):
    def __init__(self, _id):
        super().__init__(_id)
        self.id = _id

    def is_satisfied(self):
        return {'menu_id': str(self.id)}


class GetAllDishesFilter(BaseFilter):
    def __init__(self, _id):
        super().__init__(_id)
        self.submenu_id = _id

    def is_satisfied(self):
        return {'submenu_id': self.submenu_id}
