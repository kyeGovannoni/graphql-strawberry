import typing 
import uuid 
import strawberry
from strawberry.types import Info
import datetime
from GraphQLAPI.scalars.custom import Base64
from GraphQLAPI.schemas.directives import Keys
from GraphQLAPI.utils.SQL import get_sql_data, add_pyodbc_for_access_token, get_connection_string
from GraphQLAPI.utils.helper import data_to_schema_object
from azure.identity import DefaultAzureCredential
from os import environ
import decimal
# az credentials
credentials = DefaultAzureCredential()
conn_string = get_connection_string()
conn_kwargs = add_pyodbc_for_access_token(credentials)

#resolvers
def get_vendor(name:str, root:"Vendor", info: Info)-> "Vendor":
  results = get_sql_data(
      sql_statement= 'SELECT vendorId, vendor FROM vendors WHERE vendor = ?',
      parameters= ('%s'%(name),),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(Vendor, results, True) 

def get_vendor_for_taxis( root:"TaxiTrip", info: Info)-> "Vendor":
  results = get_sql_data(
      sql_statement= 'SELECT vendorId, vendor FROM vendors WHERE vendorId = ?',
      parameters= (root.vendorId,),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(Vendor, results, True) 


def get_payment_type_for_taxis( root:"TaxiTrip", info: Info)-> "PaymentType":
  results = get_sql_data(
      sql_statement= 'SELECT id, paymentType FROM paymentTypes WHERE id = ?',
      parameters= (root.paymentType,),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(PaymentType, results, True) 


def get_all_vendors(root:"Vendor", info: Info)-> typing.List["Vendor"]:
  results = get_sql_data(
      sql_statement= 'SELECT vendorId, vendor FROM vendors',
      parameters= (),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(Vendor, results, singleton=False) 

def get_payment_type(name:str, root:"PaymentType", info: Info)-> "PaymentType":
  results = get_sql_data(
      sql_statement= 'SELECT id, paymentType FROM paymentTypes WHERE paymentType = ?',
      parameters= ('%s'%(name),),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(PaymentType, results, singleton=True) 

def get_all_payment_type(root:"PaymentType", info: Info)-> typing.List["PaymentType"]:
  results = get_sql_data(
      sql_statement= 'SELECT id, paymentType FROM paymentTypes',
      parameters= (),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(PaymentType, results, singleton=False) 

def get_all_taxi_trips(root:"TaxiTrip", info: Info)-> typing.List["TaxiTrip"]:
  results = get_sql_data(
      sql_statement= 'SELECT \
                        vendorId, tpepPickupDateTime,tpepDropoffDateTime, passengerCount, tripDistance,\
                        paymentType,fareAmount,totalAmount \
                      FROM [dbo].[taxiTrips]',
      parameters= (),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(TaxiTrip, results, singleton=False) 


def get_all_taxi_trips_root_filter(root, info: Info)-> typing.List["TaxiTrip"]:
  root_mapping = {
    'Vendor':{
      'filter_statement':'vendorId = ?',
      'schema_class':TaxiTrip,
      'parameter':'root.vendorId'
              },
    'PaymentType':{
      'filter_statement':'paymentType = ?',
      'schema_class':TaxiTrip,
      'parameter':'root.id'
              },
  }

  _map = root_mapping[root.__class__.__name__]
  param = eval(_map['parameter'])
  results = get_sql_data(
      sql_statement= 'SELECT \
                        vendorId, tpepPickupDateTime,tpepDropoffDateTime, passengerCount, tripDistance,\
                        paymentType,fareAmount,totalAmount \
                      FROM [dbo].[taxiTrips] WHERE %s' % (_map['filter_statement']),
      parameters= (param,),
      connection_string=conn_string,
      kwargs=conn_kwargs
    )  
  return data_to_schema_object(TaxiTrip, results, singleton=False) 


@strawberry.type
class Vendor:
  vendorId: strawberry.Private[str]
  vendor: str 
  taxiTrips: typing.List["TaxiTrip"]= strawberry.field(resolver=get_all_taxi_trips_root_filter)
  #tag: uuid.UUID

@strawberry.type
class PaymentType:
  id: strawberry.Private[str]
  paymentType: str
  taxiTrips: typing.List["TaxiTrip"] = strawberry.field(resolver=get_all_taxi_trips_root_filter)

@strawberry.type
class TaxiTrip:
  vendorId:strawberry.Private[str]
  vendor: Vendor = strawberry.field(resolver=get_vendor_for_taxis)
  tpepPickupDateTime:str#datetime.datetime
  tpepDropoffDateTime:str#datetime.datetime
  passengerCount:int
  tripDistance:decimal.Decimal
  paymentType:strawberry.Private[str]
  payment:PaymentType = strawberry.field(resolver=get_payment_type_for_taxis)
  fareAmount:str
  totalAmount:str

@strawberry.type
class TaxisQuery:
    getVendor: Vendor = strawberry.field(resolver=get_vendor)
    getAllVendors: typing.List[Vendor] = strawberry.field(resolver=get_all_vendors)
    getPaymentType: PaymentType = strawberry.field(resolver=get_payment_type)
    getAllPaymentTypes: typing.List[PaymentType] = strawberry.field(resolver=get_all_payment_type)
    getAllTaxiTrips: typing.List[TaxiTrip] = strawberry.field(resolver=get_all_taxi_trips)



