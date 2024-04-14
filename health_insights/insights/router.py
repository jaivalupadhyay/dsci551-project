class ModelRouter:
    def db_for_read(self, model, **hints):
        """
        Routes reading operations to both databases.
        """
        return None

    def db_for_write(self, model, **hints):
        """
        Routes writing operations based on patient ID.
        """
        patient_id = hints.get('patient_id', None)
        if patient_id is not None:
            return 'db1' if int(patient_id) % 2 != 0 else 'db2'
        return None

    # def allow_relation(self, obj1, obj2, **hints):
    #     """
    #     Allow relations if two objects are in the same database.
    #     """
    #     db_obj1 = self.db_for_write(None, patient_id=obj1.patient_id)
    #     db_obj2 = self.db_for_write(None, patient_id=obj2.patient_id)
    #     return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All models end up in both databases.
        """
        return True
