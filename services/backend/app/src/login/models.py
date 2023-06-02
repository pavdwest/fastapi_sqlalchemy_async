# from src.models import AppModel, SharedModelMixin


# class Login(AppModel, SharedModelMixin):
#     email                                   = fields.CharField(max_length=1023, unique=True)
#     password_hash                           = fields.CharField(max_length=1023)
#     verified                                = fields.BooleanField(null=False, default=False)
#     name                                    = fields.CharField(max_length=1023, null=True)
#     surname                                 = fields.CharField(max_length=1023, null=True)
#     role:   fields.ForeignKeyRelation[Role] = fields.ForeignKeyField(f"{SHARED_APP_NAME}.Role")

#     async def verify(self):
#         self.verified = True


# class BelongsToLogin(BelongsToMixin):
#     login:  fields.ForeignKeyRelation[Role] = fields.ForeignKeyField(f"{SHARED_APP_NAME}.Login")


# class LoginVerification(AppModel, BelongsToLogin):
#     verification_token = fields.CharField(max_length=1023, unique=True)
