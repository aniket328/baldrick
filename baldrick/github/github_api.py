import requests

from changebot.github_auth import github_request_headers

__all__ = ['submit_review', 'set_status']


def submit_review(pull_request_payload, decision, body):
    """
    Submit a review comment to a pull request on GitHub.

    Parameters
    ----------
    pull_request_payload : dict
        The payload sent from GitHub via the webhook interface
    decision : { 'approve' | 'reject' | 'comment' }
        The decision as to whether to aprove or reject the changes so far.
    body : str
        The body of the review comment
    """

    url_review = pull_request_payload['review_comments_url'].replace('comments', 'reviews')

    data = {}
    data['commit_id'] = data['head']['sha']
    data['body'] = body
    data['event'] = decision.upper()

    headers = github_request_headers(pull_request_payload['installation'])

    requests.post(url_review, json=data, headers=headers)


def set_status(pull_request_payload, state, description, context):
    """
    Set status message in a pull request on GitHub.

    Parameters
    ----------
    pull_request_payload : dict
        The payload sent from GitHub via the webhook interface.
    state : { 'pending' | 'error' | 'pass' }
        The state to set for the pull request.
    description : str
        The message that appears in the status line.
    context : str
         A string used to identify the status line.
    """

    url_status = pull_request_payload['statuses_url']

    data = {}
    data['state'] = state
    data['description'] = description
    data['context'] = context

    headers = github_request_headers(pull_request_payload['installation'])

    requests.post(url_status, json=data, headers=headers)
