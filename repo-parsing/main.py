from parser.parser import search_repositories_with_open_issues, save_results_to_json, read_repos_from_json, send_repos_to_message_broker


if __name__ == "__main__":
  results = search_repositories_with_open_issues()
  save_results_to_json(results)

  # for repo in read_repos_from_json():
  #   send_repos_to_message_broker(repo)