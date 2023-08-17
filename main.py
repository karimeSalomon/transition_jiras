import json
from helpers.get_from_jira import GetFromJira
from helpers import df_for_releases
from datetime import datetime
from dateutil.relativedelta import relativedelta


def search_by_jql(query):
    data = {
        "jql": query,
        "fields": ['key', 'status', 'issuetype'],
        "maxResults": 100,
        "startAt": 0
    }
    get_from_jira = GetFromJira.instance()
    result = get_from_jira.post('search', json.dumps(data))
    print("The JQL is : " + query)
    return result.json()


def do_transition(issue, data):
    get_from_jira = GetFromJira.instance()
    get_from_jira.post('issue/{issue}/transitions'.format(issue=issue), data)


# Send the Key of the Jira project in this case XWZ
releases = df_for_releases.get_list_of_releases('XWZ')
# Data for transition to Deployed
data_deployed = {'transition': {'id': '241'}}
# Data for transition to Next to Deploy
data_next = {'transition': {'id': '231'}}
# Data for transition to Ready to deploy
data_ready = {'transition': {'id': '221'}}

for each_release in releases:
    # only if it was released.
    if each_release['released']:
        release_Date = each_release['releaseDate']
        # only if release date was in the last year
        if datetime.fromisoformat(release_Date) > (datetime.now() - relativedelta(years=1)):
            print(datetime.fromisoformat(release_Date))
            fixversion = each_release['id']
            print(fixversion)
            jira_issue = search_by_jql("fixVersion = " + fixversion)
            for jira_ticket in jira_issue['issues']:
                if (jira_ticket['fields']['status']['name'] != 'Deployed') and (
                        jira_ticket['fields']['status']['name'] != "Won't Fix") and (
                        jira_ticket['fields']['issuetype']['name'] != "Epic"):
                    print(jira_ticket['key'] + " IS A : " + jira_ticket['fields']['issuetype'][
                        'name'] + ' STATUS IS : ' + jira_ticket['fields']['status']['name'])
                    # If status is Accepted need to make 3 transitions until Deployed
                    if jira_ticket['fields']['status']['name'] == 'Accepted':
                        # do the transition to Ready to deploy
                        do_transition(jira_ticket['key'], json.dumps(data_ready))
                        do_transition(jira_ticket['key'], json.dumps(data_next))
                        do_transition(jira_ticket['key'], json.dumps(data_deployed))

                    # If status is Accepted need to make 2 transitions until Deployed
                    if jira_ticket['fields']['status']['name'] == 'Ready to Deploy':
                        do_transition(jira_ticket['key'], json.dumps(data_next))
                        do_transition(jira_ticket['key'], json.dumps(data_deployed))

                    # If status is Accepted need to make 1 transition until Deployed
                    if jira_ticket['fields']['status']['name'] == 'Next to Deploy':
                        # do the transitions
                        do_transition(jira_ticket['key'], json.dumps(data_deployed))
