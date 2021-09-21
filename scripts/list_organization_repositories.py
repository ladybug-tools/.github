import os
import urllib.request
import json


ACCESS_TOKEN = os.getenv('GH_TOKEN', "")
ORGANIZATION_NAME = 'ladybug-tools'


def get_organization_repositories(cursor: str = None):
    endpoint = "https://api.github.com/graphql"
    query_with_variables = """query ($login: String!, $endCursor: String) { 
            repositoryOwner(login:$login) {
            repositories(first: 50, after: $endCursor, isFork:false, isLocked: false){
            totalCount
            pageInfo{
                startCursor
                endCursor
                hasNextPage
                hasPreviousPage
            }
            nodes{
                name
            }
            }
        }
    }
    """
    jsondata = json.dumps({'query': query_with_variables, "variables": {"login": ORGANIZATION_NAME, "endCursor": cursor}})
    req = urllib.request.Request(url=endpoint, method='POST', data=jsondata.encode('utf-8') )
    req.add_header('Authorization', f'Bearer {ACCESS_TOKEN}')
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf-8'))


if __name__ == '__main__':
    has_more = True
    cursor = None
    repositories = []

    while has_more:
        res = get_organization_repositories(cursor=cursor)
        page_info = res['data']['repositoryOwner']['repositories']['pageInfo']
        repos = res['data']['repositoryOwner']['repositories']['nodes']
        for repo in repos:
            repositories.append(repo['name'])
        
        has_more = page_info['hasNextPage']
        cursor = page_info['endCursor']

    print_result = {"repository": repositories}

    print(json.dumps(print_result))