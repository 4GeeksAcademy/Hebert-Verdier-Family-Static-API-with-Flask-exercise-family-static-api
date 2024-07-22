
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = []

    # GENERAR ID AL AZAR
    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    # AGREGAR MIEMBRO
    def add_member(self, member):
        # fill this method and update the return
        if "id" not in member:
            member['id'] = self._generateId()
        self._members.append(member)
        pass

    # ACTUALIZAR MIEMBRO
    def update_member(self, id, up_member):
        # fill this method and update the return
        for member in self._members:
            if member['id'] == id:
                member['age'] = up_member['age']
                member['first_name'] = up_member['first_name']
                member['lucky_numbers'] = up_member['lucky_numbers']
        pass

    # ELIMINAR MIEMBRO
    def delete_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member['id'] == id:
                self._members.remove(member)
                return {"done": True}
        return {"done": False}

    # TRAER MIEMBRO
    def get_member(self, id):
        # fill this method and update the return
        for member in self._members:
            if member['id'] == id:
                return member
        return None

    # TRAER MIEMBROS
    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
