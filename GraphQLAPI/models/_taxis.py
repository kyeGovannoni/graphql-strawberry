import logging
from typing import TYPE_CHECKING, Annotated, List
import strawberry
from strawberry.types import Info
from GraphQLAPI.utils.SQL import get_sql_data, add_pyodbc_for_access_token, get_connection_string
from GraphQLAPI.utils.helper import data_to_schema_object
import decimal

if TYPE_CHECKING:
  from GraphQLAPI.models._vendors import Vendor
  from GraphQLAPI.models._payment_types import PaymentType

#resolvers
async def get_vendor_for_taxi_trip( root:"TaxiTrip", info: Info)-> "Vendor":
  results = get_sql_data(
      sql_statement= 'SELECT vendorId, vendor FROM vendors WHERE vendorId = ?',
      parameters= (root.vendorId,),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    )  
  from GraphQLAPI.models._vendors import Vendor
  return data_to_schema_object(Vendor, results, True) 

async def get_payment_type_for_taxi_trip( root:"TaxiTrip", info: Info)-> "PaymentType":
  results = get_sql_data(
      sql_statement= 'SELECT id, paymentType FROM paymentTypes WHERE id = ?',
      parameters= (root.paymentType,),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    ) 
  from GraphQLAPI.models._payment_types import PaymentType
  return data_to_schema_object(PaymentType, results, True) 

async def get_all_taxi_trips(root:"TaxiTrip", info: Info)-> List["TaxiTrip"]:
  results = get_sql_data(
      sql_statement= 'SELECT \
                        vendorId, tpepPickupDateTime,tpepDropoffDateTime, passengerCount, tripDistance,\
                        paymentType,fareAmount,totalAmount \
                      FROM [dbo].[taxiTrips]',
      parameters= (),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    )  
  return data_to_schema_object(TaxiTrip, results, singleton=False) 


# schemas 

@strawberry.type
class TaxiTrip:
  vendorId:strawberry.Private[str]
  vendor: Annotated["Vendor", strawberry.lazy("GraphQLAPI.models._vendors")] = strawberry.field(resolver=get_vendor_for_taxi_trip)
  tpepPickupDateTime:str#datetime.datetime
  tpepDropoffDateTime:str#datetime.datetime
  passengerCount:int
  tripDistance:decimal.Decimal
  paymentType:strawberry.Private[str]
  payment:Annotated["PaymentType", strawberry.lazy("GraphQLAPI.models._payment_types")] = strawberry.field(resolver=get_payment_type_for_taxi_trip)
  fareAmount:str
  totalAmount:str


@strawberry.type
class TaxisQuery:
    getAllTaxiTrips: List[TaxiTrip] = strawberry.field(resolver=get_all_taxi_trips)




