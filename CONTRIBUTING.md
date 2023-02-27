# Contributing

Thanks for considering contributing to the project. All contributions are appreciated.



## Submit Issues

Please select the appropriate issue label when opening a new issue.

### :bulb: Feature

Suggest a new bot feature.

### :zap: Enhancement

Suggest changes to improve an existing feature. For example, changing the format of a command response, etc.

### :bug: Bug

If something is not working as expected, file a bug report.


### :memo: Documentation

Improvements or additions to documentation



## Solve an issue

View the [existing issues](https://github.com/Yamen-Malik/PCC-Bot/issues) to find one that interests you. If you find an issue to work on, you are welcome to open a pull request with a fix.



## Pull Requests

Please follow the following guidelines when adding a poll request:

- Use the [command](commands/README.md) and [event](events//README.md) templates when adding new commands or event files to the project.
- Follow [PEP8][pep-8] guidelines in formatting python code.
- Using [Black formatter][black] is greatly recommended.
- Make sure your code has passed all [tests][github-actions] before submitting a poll request.


**Creating a poll request**

1. [Fork][fork-a-repo] the repository on GitHub.

2. [Clone][cloning-a-repo] the forked repo to your local machine.

3. Create a new [feature branch][feature-branch] from master

4. Commit your changes

5. Push your changes back up to your fork.

6. When you're ready, submit a [pull request][pull-requests] so that we can review your changes.

Don't forget to [link poll request to issue][link-PR-to-issue] if you are solving one.

If you have an existing fork, make sure to [sync][sync-fork-with-upstream] the latest changes from the upstream repository before working on a new contribution.

```shell
$ git remote add upstream https://github.com/Yamen-Malik/PCC-Bot.git
$ git pull upstream master
```

You may be asked for changes to be made before a poll request can be merged.

Once your poll request is merged, your contributions will be publicly visible on the repository page.

[fork-a-repo]: https://help.github.com/en/articles/fork-a-repo
[cloning-a-repo]: https://help.github.com/en/articles/cloning-a-repository
[feature-branch]: https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow
[pull-requests]: https://help.github.com/en/articles/about-pull-requests
[pep-8]: https://peps.python.org/pep-0008/
[black]: https://github.com/psf/black
[github-actions]: https://github.com/Yamen-Malik/PCC-Bot/actions
[link-PR-to-issue]: https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue
[sync-fork-with-upstream]: https://docs.github.com/en/get-started/quickstart/fork-a-repo#configuring-git-to-sync-your-fork-with-the-upstream-repository