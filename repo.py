import os
import subprocess as sub
import shlex
from dateutil import parser


class Repo:

    def __init__(self):
        self.path = None
        self.commits = []
        self._read = False
        self._log_format = ['%H', '%an', '%ae', '%s', '%ad']
        self._log_field = ['id', 'author_name', 'author_email',
                           'subject', 'date']

    def __len__(self):
        return len(self.commits)

    def __iter__(self):
        for commit in self.commits:
            yield commit

    def read_repo(self, path, month):
        log_format = '%x1f'.join(self._log_format)
        log_format = '%x1e' + log_format
        exp = "git log --no-merges --numstat --since=" \
              + str(month) + "month"
        exp += " "  # avoiding error due to no space btn next expression
        exp = exp + " --format=" + "'" + log_format + "'"
        os.chdir(path)
        p = sub.Popen(shlex.split(exp), stdout=sub.PIPE, stderr=sub.PIPE)
        (log, _) = p.communicate()
        self._parse_log(log)

    def _parse_log(self, log):
        assert log, "empty log"

        log = log.split('\x1e')
        log.pop(0)  # first item is always empty
        for raw_commit in log:
            self._parse_commit(raw_commit)

    def _parse_commit(self, raw_commit):
        assert raw_commit, "empty raw_commit"

        raw_commit = raw_commit.split('\n')
        raw_commit.pop()  # last item is always empty
        summary = raw_commit.pop(0)
        summary = dict(zip(self._log_field, summary.split('\x1f')))
        raw_commit.pop(0)  # next item is alwaus empty
        diffs = []
        diff_field = ['ins', 'del', 'filename']
        for diff in raw_commit:
            diff = diff.split('\t')
            diff = [int(ii) if ii.isdigit() else ii for ii in diff]
            diffs.append(dict(zip(diff_field, diff)))
        commit = {}
        commit.update(summary)
        commit['change'] = diffs
        commit['date'] = parser.parse(commit['date'])
        self.commits.append(commit)
