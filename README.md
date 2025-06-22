# sigmoid-summer-hackathon-2025-backend | ContributeIT

## Description

What’s one of the best ways for a developer to apply their technical skills and gain valuable hands-on experience outside of a traditional job ( * job application screamer * )? Contributing to open source!
But finding the right project that matches your skills and interests can be overwhelming. That’s where ContributeIT comes in — a platform that aggregates and filters GitHub repositories that are open for contributions, helping you discover the perfect fit.

## Architecture

![Architecture](./architecture.png)

## Backend API

The backend is a `monolithic Django` (DRF) application, handling `user account`, `performance metrics`, and `repository data` within a single service. Authentication is implemented using `GitHub OAuth` for user identity and `JWT` for session management.

### Authentication

Authentication begins with the frontend redirecting the user to https://github.com/login/oauth/authorize, including the GitHub Client ID and callback URI as query parameters. After the user authorizes access, GitHub redirects to the specified callback URI with an authorization code. This code must then be sent in the payload of a POST request to the /auth/callback/ endpoint. In response, the client receives a pair of JWT tokens (access and refresh) along with the user's information, which is then used to populate the profile page.

### Business Endpoints

The backend is deployed on `Google Cloud Platform (GCP)` and is available for testing at: https://app-242229169063.europe-central2.run.app.

0. GET / - `healthcheck` endpoint to verify that the server is running

1. GET /repos/filters-list/ - enables the frontend to fetch the list of all supported filters

    Expects: -

    Returns:

        {
            "pref_langs":   string[] - all the programming languages supported for filtering,
            "pref_domains": string[] - all the programming domains supported for filtering
        }

2. PATCH /users/update-user-prefs/ - allows the user to update (overwrite) their `preferences`

    Expects (+ bearer access token in the _Authorization_ header):
        
        {
            "pref_langs":   string[] - ...,
            "pref_domains": string[] - ...
        }

    Returns:

        A success message

    

3. POST /repos/create/ - allows the worker to create or update `discovered repository records` in the database

    Expects (+ worker's secret in a custom header):

        {
            "name":         string — the display name of the repository",
            "url":          string — repository's GitHub URL",
            "stars":        int — number of stars the repository has",
            "forks":        int — number of forks the repository has",
            "langs":        string[] — list of programming languages featured in the project",
            "domains":      string[] — list of programming domains featured in the project",
            "good_first":   boolean — indicates if the repository has issues labeled as 'good first issue'"
        }

    Returns:

        The response contains the serialized representation of the created record, structured identically to the input payload

4. GET /repos/search/ - `paginated and filtered listing` of platform-aggregated repositories

    Expects:
        
        * domain, lang, good_first - filters are passed as query parameters (omit any that aren’t needed; do not include empty parameters in the URL)
        * page - select a part of the queriset

    Returns:
        
        {
            "count":    int - the count of items returned (results),
            "next":     string - a string containing the URL to the next page of results,
            "previous": string - a string containing the URL to the previous page of results.,
            "results":  [
                            {
                                ... (lookup /repos/create/ documentation),
                            }
                        ]
        }

## Repository Discovery Pipeline

The pipeline consists of the three main modules: `repository parser`, `repository worker` and `openai integration`. 

The parser periodically searches Github repositories (using Github API) to discover open-source projects with pending issues for contribution and pushes the information about every repo to a `rabbitmq` queue.
 
The workers consume the data about repositories sent to the queue, process it using `openai` integration to extract domains used in the filtering and the post them to the database via backend API. 

In order to test this module it is neccessary to run both parser and the worker, the simplest setup is the following:

```
  # from the repo-parsing/broker folder
  python worker.py

  # after that from the repo-parsing folder
  python main.py
```

After the `parser` finishes its execution the `worker` will be waiting for new information about currently featured repositories pushed to the queue.