from github import Github
from dotenv import load_dotenv
import os
import json
from broker.message_broker import get_rabbitmq_channel
from ai.openai import get_repository_topics


MAX_CHARS = 8000

load_dotenv()
github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
query = "is:public license:mit archived:false issues:>1 stars:>1"


def search_repositories_with_open_issues():
  result = []

  try:
    repositories = github.search_repositories(query=query, sort="stars", order="desc")

    for repo in repositories:
      if repo.open_issues_count > 0:
        open_issues = []

        for issue in repo.get_issues(state="open"):
          if issue.pull_request is not None:        
            continue

          open_issues.append({
              "title": issue.title,
              "url": issue.html_url,
              "labels": [label.name for label in issue.labels],
          })

        repo_info = {
          "name": repo.name,
          "owner": repo.owner.login,
          "url": repo.html_url,
          "domains": get_repository_topics(repo.description[:MAX_CHARS]) if repo.description else [],
          "languages": list(repo.get_languages().keys()),
          "topics": repo.get_topics(),
          "stars": repo.stargazers_count,
          "open_issues": open_issues,
        }

        result.append(repo_info)
  except Exception as e:
    print(f"An error occurred: {e}")

  return result


def save_results_to_json(results, filename="repos.json"):
  if os.path.exists(filename):
    os.remove(filename)

  with open(filename, "w+", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)


def send_repos_to_message_broker(repos):
  connection, channel = get_rabbitmq_channel()
  
  for repo in repos:
    channel.basic_publish(
      exchange='',
      routing_key='repos',
      body=json.dumps(repo, ensure_ascii=False).encode('utf-8')
    )

  connection.close()
