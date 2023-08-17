from helpers.get_from_jira import GetFromJira


def get_list_of_releases(project_key):
    """
         Performs GET method to JIRA project by Key
         :param project_key: JIRA project KEY
         :return: List of Releases by the project Key
    """
    get_from_jira = GetFromJira.instance()
    project_id = get_from_jira.get_id_from_project(project_key)
    # Get all releases by project
    all_info_releases = get_from_jira.get_all_releases_from_project(project_id)

    return all_info_releases
