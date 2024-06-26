
import json
import azure.functions as func
from azure.cosmos import CosmosClient

# Initialize CosmosClient with account endpoint and account key
endpoint = "Your Endpoint"
key = "Your Keys"
client = CosmosClient(endpoint, credential=key)

# Specify the name of your database and container
database_name = "Database Name"
container_name = "Cointainer Name"
item_id = "ID"

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="GetResumeCounter")
def GetResumeCounter(req: func.HttpRequest) -> func.HttpResponse:
        
    # Retrieve current count item
    count_item = container.read_item(item_id, item_id)

    # Validate the required parameters
    if not count_item:
        return func.HttpResponse(
            "Count item missing",
            status_code=400  # Bad Request
        )
    
    # Extract the integer property from the item
    current_count = count_item.get('count', 0)

    # increment the count for each page refresh/API call
    updated_count = current_count + 1

    # Update the count item with the new value
    count_item['count'] = updated_count
    container.upsert_item(count_item)
    
    # Serialize the item to JSON
    item_json = json.dumps(count_item, indent=2)

    # Return the item as a JSON response
    return func.HttpResponse(
        body=item_json, 
        mimetype='application/json',
        status_code=200
    )

    

    

    