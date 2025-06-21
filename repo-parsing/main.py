from parser.parser import search_repositories_with_open_issues, save_results_to_json, send_repos_to_message_broker


if __name__ == "__main__":
  results = search_repositories_with_open_issues()
  save_results_to_json(results)
  # send_repos_to_message_broker(results)