from marshmallow import Schema, fields

#Plain schemas
class PlainCustomerSchema(Schema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    gender = fields.Str(required=True)
    age = fields.Int(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)

class PlainMerchantSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    industry = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    long = fields.Float(required=True)
    lat = fields.Float(required=True)

class PlainAccountSchema(Schema):
    id = fields.Str(dump_only=True)
    currency = fields.Str(required=True)
    balance = fields.Float(required=True)
    movement = fields.Str(required=True)
    customer_id = fields.Str(required=False)

class PlainTransactionSchema(Schema):
    id = fields.Str(dump_only=True)
    date = fields.DateTime(required=True)
    status = fields.Str(required=True)
    card_present_flag = fields.Int(required=True)
    bpay_biller_code = fields.Str(required=True)
    long = fields.Float(required=True)
    lat = fields.Float(required=True)
    txn_description = fields.Str(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True)
    movement = fields.Str(required=True)
    merchant_id = fields.Str(required=True)
    customer_id = fields.Str(required=True)
    account_id = fields.Str(required=True)
    score_id = fields.Str(required=False)

class PlainScoreSchema(Schema):
    id = fields.Str(dump_only=True)
    score = fields.Float(required=False)
    datetime = fields.DateTime(required=False)

#Update schemas
class CustomerUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    gender = fields.Str()
    age = fields.Int()
    city = fields.Str()
    state = fields.Str()

class MerchantUpdateSchema(Schema):
    name = fields.Str()
    industry = fields.Str()
    city = fields.Str()
    state = fields.Str()
    long = fields.Float()
    lat = fields.Float()

class AccountUpdateSchema(Schema):
    currency = fields.Str()
    balance = fields.Float()
    movement = fields.Str()
    customer_id = fields.Str()

class TransactionUpdateSchema(Schema):
    score_id = fields.Str()

class ScoreUpdateSchema(Schema):
    score = fields.Float()
    datetime = fields.DateTime()

#Creation schemas
class CustomerSchema(PlainCustomerSchema):
    accounts = fields.List(fields.Nested(PlainAccountSchema()), dump_only=True)
    #Review later, this must return a list of lists (every transaction for a customer)
    transactions = fields.List(fields.Nested(PlainTransactionSchema()), dump_only=True)

class MerchantSchema(PlainMerchantSchema):
    #Review later, this must return a list of lists (every transaction for a merchant)
    transactions = fields.List(fields.Nested(PlainTransactionSchema()), dump_only=True)

class AccountSchema(PlainAccountSchema):
    customer_id = fields.Str(required=True, load_only=True)
    customer = fields.List(fields.Nested(PlainCustomerSchema()), dump_only=True)

class TransactionSchema(PlainTransactionSchema):
    merchant = fields.List(fields.Nested(PlainMerchantSchema()), dump_only=True)
    customer = fields.List(fields.Nested(PlainCustomerSchema()), dump_only=True)
    account = fields.List(fields.Nested(PlainAccountSchema()), dump_only=True)
    score = fields.List(fields.Nested(PlainScoreSchema()), dump_only=True)

class ScoreSchema(PlainScoreSchema):
    transaction_id = fields.Str(required=True, load_only=True)
    transaction = fields.List(fields.Nested(PlainTransactionSchema()), dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)