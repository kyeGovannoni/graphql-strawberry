from typing import TYPE_CHECKING, Annotated, List, Optional
import strawberry
from strawberry.types import Info
from GraphQLAPI.utils.SQL import get_sql_data, add_pyodbc_for_access_token, get_connection_string
from GraphQLAPI.utils.helper import data_to_schema_object

if TYPE_CHECKING:
    from GraphQLAPI.models._taxis import TaxiTrip

# resolvers
# // taxi trip resolver
async def get_taxi_trips_for_vendor(root, info: Info)-> List["TaxiTrip"]:
  results = get_sql_data(
      sql_statement= 'SELECT \
                        vendorId, tpepPickupDateTime,tpepDropoffDateTime, passengerCount, tripDistance,\
                        paymentType,fareAmount,totalAmount \
                      FROM [dbo].[taxiTrips] WHERE vendorId  = ?',
      parameters= (root.vendorId,),
      connection_string=get_connection_string(),
      kwargs=add_pyodbc_for_access_token(None)
    )  
  # need to actually import the module class. 
  from GraphQLAPI.models._taxis import TaxiTrip
  return data_to_schema_object(TaxiTrip, results, singleton=False) 

# singleton vendor resolver. 
async def get_vendor(name:str, root:"Vendor", info: Info)-> "Vendor":
   results = get_sql_data(
       sql_statement= 'SELECT vendorId, vendor FROM vendors WHERE vendor = ?',
       parameters= ('%s'%(name),),
       connection_string=get_connection_string(),
       kwargs=add_pyodbc_for_access_token(None)
     )  
   return data_to_schema_object(Vendor, results, True) 

# list of vendors resolver.
async def get_all_vendors(root:"Vendor", info: Info)-> List["Vendor"]:
   results = get_sql_data(
       sql_statement= 'SELECT vendorId, vendor FROM vendors',
       parameters= (),
       connection_string=get_connection_string(),
       kwargs=add_pyodbc_for_access_token(None)
     )  
   return data_to_schema_object(Vendor, results, singleton=False) 


# schemas 
@strawberry.type
class Vendor:
  vendorId: strawberry.Private[str]
  vendor: str 
  taxiTrips: None |List[None | Annotated["TaxiTrip", strawberry.lazy("GraphQLAPI.models._taxis")]] = strawberry.field(resolver=get_taxi_trips_for_vendor)

@strawberry.type
class VendorQuery:
    getVendor: Vendor = strawberry.field(resolver=get_vendor)
    getAllVendors: List[Vendor] = strawberry.field(resolver=get_all_vendors)
   
