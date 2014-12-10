import os
import subprocess as sub
import shlex
from dateutil import parser


class Repo:

    def __init__(self):
        self._path = None
        self._commits = []
        self._log_format = ['%H', '%an', '%ae', '%s', '%ad']
        self._log_field = ['id', 'author_name', 'author_email',
                           'subject', 'date']

    def __len__(self):
        return len(self._commits)

    def __iter__(self):
        for commit in self._commits:
            yield commit

    @property
    def path(self):
        return self._path

    def read_repo(self, path, month):
        self._path = path
        log_format = '%x1f'.join(self._log_format)
        log_format = '%x1e' + log_format
        exp = "git log --no-merges --numstat --since=" \
              + str(month) + "month"
        exp += " "  # avoiding error due to no space btn next expression
        exp = exp + " --format=" + "'" + log_format + "'"
        current_dir = os.getcwd()
        os.chdir(self._path)
        p = sub.Popen(shlex.split(exp), stdout=sub.PIPE, stderr=sub.PIPE)
        (log, _) = p.communicate()
        self._parse_log(log)
        os.chdir(current_dir)

    def _parse_log(self, log):
        assert log, "log is empty"

        log = log.split('\x1e')
        log.pop(0)  # first item is always empty
        for raw_commit in log:
            self._parse_commit(raw_commit)

    def _parse_commit(self, raw_commit):
        assert raw_commit, "raw_commit is empty: %r" % raw_commit

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
        self._commits.append(commit)
