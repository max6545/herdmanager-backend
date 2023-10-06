from flask_restful import reqparse

user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument('name', required=True, location=('json',), help="name is required parameter!")
user_parser.add_argument('password', required=True, location=('json',), help="password is required parameter!")

sheep_parser = reqparse.RequestParser(bundle_errors=True)
sheep_parser.add_argument('name', required=True, location=('json',), help="name is required parameter!")
sheep_parser.add_argument('individual_code', required=True, location=('json',),
                          help="individual_code is required parameter!")
sheep_parser.add_argument('father_id', required=False, location=('json',))
sheep_parser.add_argument('mother_id', required=False, location=('json',))
