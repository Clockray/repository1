import json
import sys
import urllib.request
import urllib.parse

#Get token from https://github.com/settings/tokens
#Need read permissions for public repository
ghe_header = {"Authorization": "token <<<TOKEN GOES HERE>>>" }

#GraphQL query   
graph_query = """
{
   repository(name: "repository1", owner: "Clockray") {
      object(expression: "master:bigfile.txt") {
         ... on Blob {
            text
			byteSize
         }
      }
   }
}
"""

#Github Graph version 4
#This function takes a GraphQL and runs it against the Github API address
def run_query(query):
	data = {'query': query}
	formatted_data = json.dumps(data).encode('utf-8')
	requestobject = urllib.request.Request("https://api.github.com/graphql",formatted_data,ghe_header)
	requestobject.method = 'POST'
	try:
		response = urllib.request.urlopen(requestobject)
		return response
	except urllib.error.HTTPError as error:
		print((error.read()))
		
result = run_query(graph_query) 
resulting_byte_content = result.read()
resulting_json = json.loads(resulting_byte_content.decode('utf8'))
print ("Res JSON start is:",str(resulting_json)[0:30])
print ("Res JSON end is  :",str(resulting_json)[-30:])
print ("Size of bytes content is:",sys.getsizeof(resulting_byte_content))
print ("Size of downloaded text JSON is:",sys.getsizeof(resulting_json["data"]["repository"]["object"]["text"]))
print ("Real size of file in Repo:",resulting_json["data"]["repository"]["object"]["byteSize"])

"""Observed output is:
Res JSON start is: {'data': {'repository': {'obje
Res JSON end is  : 6789', 'byteSize': 1716680}}}}
Size of bytes content is: 512098
Size of resulting JSON is: 512049
"""

sys.exit()