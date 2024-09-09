from fastapi import FastAPI, HTTPException, Query
from typing import Union
import httpx 
import os
from dotenv import load_dotenv
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
load_dotenv()  # Load the environment variables
os.environ["LLAMA_CLOUD_API_KEY"] = os.getenv("LLAMA_CLOUD_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


app = FastAPI()

index = LlamaCloudIndex(
    name="stanford_law_4_full_default", 
    project_name="Default",
    organization_id="2375fb00-b78c-41a4-b1af-ee7b7ff18f51",
)



# Define the external endpoint to which we'll forward the query
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/posts"  # Example URL, replace with your endpoint

@app.get("/forward-query/")
async def forward_query(query: str):
    """
    Takes a query string as input, sends it to another endpoint, and returns the response.
    
    Args:
    - query: The query string to be forwarded to the external endpoint.
    
    Returns:
    - JSON response from the external API.
    """
    try:
        # Send the query to the external API endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(EXTERNAL_API_URL, params={"query": query})
        
        # Check if the external API request was successful
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from external API.")
        
        # Return the response from the external API
        return response.json()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





@app.get("/query")
def read_root():
    index = LlamaCloudIndex(
    name="stanford_law_4_full_default", 
    project_name="Default",
    organization_id="2375fb00-b78c-41a4-b1af-ee7b7ff18f51",
    )

    # # add openai embedding

    # # from llama_cloud_index.embeddings.openai import OpenAIEmbedding
    # # Initialize the OpenAI embedding model
    #embedding_model = OpenAIEmbedding(model="text-embedding-ada-002", api_key=os.getenv("OPENAI_API_KEY"))
    #index.set_embedding_model(embedding_model)


    query_1 = "Dr. Wright testified that he did not remember if he sent bitcoin to himself or to Dave Kleinman.  What is the date of the first bitcoin coin transaction and what are the pages that information is located on?"

    query_2 = "In the Satashoi Affair, Dr. Write is quoted as telling the Respondent the bitcoins were sent to 'Hal, Dave, [Wright] and another person'.  Provide the date of the transaction and page numbers of the nodes containing the information?"

    query_3 = "Did Dr. Write testified that he mined bitcoin wth Dave?  Provide all the page number concering his position on this issue."

    query_4 = "The applicants have not simply chosen easy route of going to a writer for information they could have gotten elsewhere. In respect of Dr. Wright, the applicants have relentlessly pursued him for discovery, yet he is proved dishonest and invasive to the extent, that the court was required to sanction him for his misbehavior.  Provide the page number concering thsi fact."


    query_5 = "to get this thing because it's working all I'm doing right now is screwing around with prompts to create examples. Do you want to push the code?The applicants have not simply chosen easy route of going to a writer for information they could have gotten elsewhere. In respect of Dr. Wright, the applicants have relentlessly pursued him for discovery, yet he is proved dishonest and invasive to the extent, that the court was required to sanction him for his misbehavior.  Provide the page number concering thsi fact."


    nodes = index.as_retriever().retrieve(query_3)
    response = index.as_query_engine().query(query_3)

    print(nodes)
    print("-----------------------------------")
    print(response)
    return {"Response" : response }



@app.get("/query")
def query_index(user_query: str = Query(..., description="The query to search within the LlamaCloudIndex")):
    """
    Endpoint to query the LlamaCloudIndex with a user-provided query string.
    
    Args:
    - user_query: The query string provided by the user.

    Returns:
    - A JSON response containing the retrieved information from the index.
    """
    try:
        # Retrieve nodes and get the response using the user-provided query
        nodes = index.as_retriever().retrieve(user_query)
        response = index.as_query_engine().query(user_query)
        
        # Debug prints for nodes and response
        print("Retrieved Nodes:", nodes)
        print("-----------------------------------")
        print("Query Response:", response)
        
        return {"Response": response}

    except Exception as e:
        print(f"Error querying the index: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the query.")

