#!/usr/bin/env python
from collections import defaultdict, OrderedDict
from time import sleep
from datetime import datetime

import requests
from pygithub3 import Github

# User configuration
OAUTH_TOKEN = 'your-oauth-token'
ORG = 'your-org-name'
DEFAULT_LIMIT = 25  # Leaderboards are limited by default, use -1 for unlimited
# End configuration. Do not edit below this line.

GH = Github(login=OAUTH_TOKEN, password='x-oauth-basic')
REQUESTS_AUTH = (OAUTH_TOKEN, 'x-oauth-basic')


class UserReport(object):
    def __init__(self):
        self.commits = 0
        self.additions = 0
        self.deletions = 0
        self.repos = 0
        self.earliest_week = 0

    def update_earliest_week(self, value):
        if self.earliest_week == 0 or value < self.earliest_week:
            self.earliest_week = value

    def __unicode__(self):
        earliest_week = datetime.fromtimestamp(int(self.earliest_week)).date()

        return "{}   {:>3} repos\n{:>78}\n".format(
            render_commit_data(self.commits, self.additions, self.deletions),
            self.repos,
            "since %s" % earliest_week)


class StatsNotYetGeneratedException(Exception):
    pass


def get_repo_stats(repo, retries=5):
    url = 'https://api.github.com/repos/%s/%s/stats/contributors' % (
        ORG, repo)
    response = requests.get(url, auth=REQUESTS_AUTH)
    attempts = 0
    cool_down = 3

    while response.status_code == 202 and attempts < retries:
        attempts += 1
        sleep(pow(cool_down, attempts))
        response = requests.get(url, auth=REQUESTS_AUTH)

    if response.status_code == 202:
        raise StatsNotYetGeneratedException

    # Repo has no stats.
    if response.status_code == 204:
        return None

    return response.json()


def accumulate_stats(weeks):
    commits = 0
    additions = 0
    deletions = 0
    earliest_week = 0

    for week in weeks:
        if week['c'] == 0:
            continue

        if int(week['w']) < earliest_week or earliest_week == 0:
            earliest_week = int(week['w'])

        commits += week['c']
        additions += week['a']
        deletions += week['d']

    return commits, additions, deletions, earliest_week


def render_commit_data(commits, additions, deletions):
    return "{:>7} commits   {:>7} ++   {:>7} --".format(
        commits, additions, deletions)


def render_header(header):
    return "\n{:=^78}\n".format(header)


def render_reports(reports, limit=DEFAULT_LIMIT):
    output = ""

    for rank, (user, report) in enumerate(reports.items(), 1):
        output += "{:>4} {:>15}: {}\n".format(
            '%s.' % rank, user, unicode(report))

        if rank == limit:
            break

    return output


def main():
    reports = defaultdict(UserReport)

    for repo in GH.repos.list_by_org('yola', type='all').iterator():
        print(render_header("Stats for %s/%s" % (ORG, repo.name)))

        stats = get_repo_stats(repo.name)

        if stats is None:
            print("No stats for this repo. Skipping...")
            continue

        for dataset in stats:
            author_username = dataset['author']['login']
            user_report = reports[author_username]

            commits, additions, deletions, earliest_week = accumulate_stats(
                dataset['weeks'])

            print("{:>15}: {}".format(
                author_username,
                render_commit_data(commits, additions, deletions)))

            user_report.update_earliest_week(earliest_week)
            user_report.repos += 1
            user_report.commits += commits
            user_report.additions += additions
            user_report.deletions += deletions

    print(render_header("Leader Boards"))

    commit_rankings = OrderedDict(
        sorted(reports.items(), key=lambda t: t[1].commits, reverse=True))
    addition_rankings = OrderedDict(
        sorted(reports.items(), key=lambda t: t[1].additions, reverse=True))
    deletion_rankings = OrderedDict(
        sorted(reports.items(), key=lambda t: t[1].deletions, reverse=True))

    print("Number of commits: \n")
    print(render_reports(commit_rankings))

    print("Lines of code added: \n")
    print(render_reports(addition_rankings))

    print("Lines of code deleted: \n")
    print(render_reports(deletion_rankings))

    print("\n* Note: This only includes stats from master branches.")

    print("\n* Note: Contributors are not limited to %s members." % ORG)

if __name__ == "__main__":
    main()
