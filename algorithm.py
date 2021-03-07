import requests
from multiprocessing import Process
import math
from pathlib import Path
import pandas as pd
import traceback
import os

github_token = os.getenv("GITHUB_ACCESS_TOKEN",None)
dirpath = os.getcwd()
filepath =  os.path.join(dirpath,'output.csv')

per_page = 100

if github_token:
    final_authorization = "token " + github_token
    headers = {
        'Accept': 'application/vnd.github.v3.star+json',
        'Authorization': final_authorization
    }
else:
    headers = {
        'Accept': 'application/vnd.github.v3.star+json'
    }


class writing_to_document():
    def __init__(self):
        self.header_values = ['starred_at', 'user']
        self.df = pd.DataFrame()

    def append_dataframe(self, data:pd.DataFrame):
        self.df = self.df.append(data,ignore_index=True)

    def generating_final_csv_file(self):
        my_file = Path(filepath)
        if my_file.exists():
            self.df.to_csv(filepath, mode='a', index=False, header=None)
        else:
            self.df.to_csv(filepath, index=False, header=self.header_values)


def generate_data(page:int, github_owner_name: str, github_project_name: str, per_page:int=100):
    '''
    Generates data in csv format
    :param page:
    :param github_owner_name:
    :param github_project_name:
    :param per_page:
    :return: None
    '''
    response = get_star_history_per_page(github_owner_name, github_project_name, page, per_page)
    csv_generator = writing_to_document()
    csv_generator.append_dataframe(response)
    csv_generator.generating_final_csv_file()

def get_star_history_per_page(github_owner_name: str, github_project_name: str, page=1, per_page=100)->dict:
    '''
    :param github_owner_name:
    :param github_project_name:
    :param page:
    :param per_page:
    :return: star count history per page
    '''
    query_url = 'https://api.github.com/repos/' + github_owner_name + '/' + github_project_name + '/stargazers'
    response = requests.get(query_url, headers=headers, params={"page": page, "per_page": per_page})
    return response.json()

def get_total_star_count_response(github_owner_name: str, github_project_name: str) -> requests.Response:
    '''
    :param github_owner_name:
    :param github_project_name:
    :return: total star count for a particular repo
    '''
    query_url = 'https://api.github.com/repos/' + github_owner_name + '/' + github_project_name
    response = requests.get(query_url, headers=headers)
    return response


def prepare_error_response(ERROR: str) -> dict:
    """
    returns error response in case of error
    """
    error_response = {
        'success': False,
        'errorMessage': str(ERROR),
    }
    return error_response


def main_function(github_owner_name: str, github_project_name: str) -> dict:
    '''
    :param github_owner_name:
    :param github_project_name:
    :return: whether the csv file generation was successful or not
    '''
    total_star_count_response = get_total_star_count_response(github_owner_name, github_project_name)
    try:
        total_star_count = int(total_star_count_response.json()['stargazers_count'])
    except:
        response = prepare_error_response(total_star_count_response.json())
        print(traceback.format_exc())
        return response

    total_pages = int(math.ceil(total_star_count / (per_page)))

    try:
        processes = []
        for page in range(1, total_pages + 1):
            pool = Process(target=generate_data, args=(page,github_owner_name, github_project_name, per_page))
            pool.start()
            processes.append(pool)

            for process in processes:
                process.join()
        return {
            'success': True
        }
    except Exception as error:
        response = prepare_error_response(str(error))
        print(traceback.format_exc())
        return response