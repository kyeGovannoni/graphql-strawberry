
from typing import TYPE_CHECKING, Annotated, List
import strawberry
from strawberry.types import Info
from GraphQLAPI.utils.SQL import get_sql_data, add_pyodbc_for_access_token, get_connection_string
from GraphQLAPI.utils.helper import data_to_schema_object

# type checking for circular imports.
if TYPE_CHECKING:
    from GraphQLAPI.models._taxis import TaxiTrip

#resolvers

# // taxi trip resolver
async def get_taxi_trips_for_payment_type(root, info: Info)-> List["TaxiTrip"]:
  results = get_sql_data(
      sql_statement= 'SELECT \
                        vendorId, tpepPickupDateTime,tpepDropoffDateTime, passengerCount, tripDistance,\
                        paymentType,fareAmount,totalAmount \
                      FROM [dbo].[taxiTrips] WHERE paymentType  = ?',
      parameters= (root.id,),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    )  
  # need to actually import the module class. 
  from GraphQLAPI.models._taxis import TaxiTrip
  return data_to_schema_object(TaxiTrip, results, singleton=False) 

# // payment resolver.
async def get_payment_type(name:str, root:"PaymentType", info: Info)-> "PaymentType":
    results = get_sql_data(
      sql_statement= 'SELECT id, paymentType FROM paymentTypes WHERE paymentType = ?',
      parameters= ('%s'%(name),),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    )  
    return data_to_schema_object(PaymentType, results, singleton=True) 

# // all payments resolver.
async def get_all_payment_types(root:"PaymentType", info: Info)-> List["PaymentType"]:
    results = get_sql_data(
        sql_statement= 'SELECT id, paymentType FROM paymentTypes',
        parameters=(),
        connection_string=get_connection_string(),
        kwargs=add_pyodbc_for_access_token(None)
      )  
    return data_to_schema_object(PaymentType, results, singleton=False) 


# Schemas.
@strawberry.type
class PaymentType:
  id: strawberry.Private[str]
  paymentType: str
  taxiTrips: List[Annotated["TaxiTrip", strawberry.lazy("GraphQLAPI.models._taxis")]] = strawberry.field(resolver=get_taxi_trips_for_payment_type)

# Base Query Type.
@strawberry.type
class PaymentTypeQuery:
    getPaymentType: PaymentType = strawberry.field(resolver=get_payment_type)
    getAllPaymentTypes: List[PaymentType] = strawberry.field(resolver=get_all_payment_types)

