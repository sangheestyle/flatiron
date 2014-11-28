# Code Snippets

You can add some code snippets for reference.

### Finding most changed files in git
[SO link](http://stackoverflow.com/questions/7686582/finding-most-changed-files-in-git)
```sh
$ git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10
```
