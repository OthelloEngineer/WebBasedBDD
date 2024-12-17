import os

import git
from git import NULL_TREE
from pydantic import BaseModel


class FileChange(BaseModel):
    file_name: str
    timestamp: str
    commit_sha: str
    before: str
    after: str
    user: str | None = None


class ChangeTracker:
    def __init__(self, basedir=None, actor_name='general', actor_email='general@example.com'):
        self._basedir = basedir if basedir else "WebBasedSolution_GIT/dk.sdu.bdd.xtext.parent/dk.sdu.bdd.xtext.examples/src/dk/sdu/bdd/xtext/examples/"
        self.repo_url = "../" 
        self.actor_name = actor_name
        self.actor_email = actor_email
        self._changes = []
        self.repo = git.Repo(self.repo_url)
        self.first_commit = "41a1ec2e53e6b74530336ef39ed7d8c6ab66dfcb"

    def set_actor(self, actor_name, actor_email=None):
        """
        Sets the actor's name and optionally their email.

        Parameters:
            actor_name (str): The name of the actor.
            actor_email (str, optional): The email of the actor. If not provided, a default is generated.
        """
        self.actor_name = actor_name
        if actor_email:
            self.actor_email = actor_email
        else:
            self.actor_email = f"{actor_name.replace(' ', '_')}@BDDWeb.com"

    def track_changes(self):
        """
        Stages all changes in the repository and commits them with the specified actor as the author.
        """
        self.repo.git.add(self._basedir)

        if self.repo.is_dirty(untracked_files=True):
            author = git.Actor(self.actor_name, self.actor_email)
            self.repo.index.commit(f"Committed by {self.actor_name}", author=author)
            print(f"Changes have been committed by {self.actor_name}.")
        else:
            print("No changes to commit.")

    def get_changes(self):
        """
        Retrieves all FileChanges made by the actor.
        """
        commits = list(self.repo.iter_commits('--all', max_count=100, since='300.days.ago', paths=self._basedir))
        changes = []
        prev_commit = NULL_TREE
        for commit in commits:
            print(f"SHA: {commit.hexsha}")
            author = commit.author
            prev_author = commit.author.name
            if prev_commit != NULL_TREE:
                prev_author = prev_commit.author.name

            print(f"Author: {author.name} <{author.email}>: current actor: {self.actor_name} <{self.actor_email}>")
            if author.name == self.actor_name:
                print(f" Found a commit by {self.actor_name} - {author.name}")
                for change in commit.diff(prev_commit):
                    if change.a_blob is None or change.b_blob is None:
                        continue
                    a_diff = change.a_blob.data_stream.read().decode('utf-8')
                    b_diff = change.b_blob.data_stream.read().decode('utf-8')
                    changes.append(
                        FileChange(file_name=change.a_path, commit_sha=commit.hexsha, before=a_diff,
                                   after=b_diff, user=commit.author.name,
                                   timestamp=commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')))
                    print(f"A_DIFF:\n{a_diff}\nB_DIFF\n{b_diff}")
            prev_commit = commit
        return changes

    def get_file_changes(self, file_path):
        path = f"{self._basedir}{file_path}"
        commits = list(self.repo.iter_commits(paths=path))

        changes = []

        prev_commit = NULL_TREE
        for commit in commits:
            diff = commit.diff(prev_commit)
            for change in diff.iter_change_type('M'):
                if file_path in change.a_path:
                    print(f"File {path} has been modified in commit {commit}.")

                    a_diff = change.a_blob.data_stream.read().decode('utf-8')
                    b_diff = change.b_blob.data_stream.read().decode('utf-8')

                    prev_author = commit.author.name
                    if prev_commit != NULL_TREE:
                        prev_author = prev_commit.author.name

                    changes.append(
                        FileChange(file_name=file_path, commit_sha=commit.hexsha, before=a_diff, after=b_diff, user=prev_author,
                                   timestamp=str(commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')))
                    )
                    print(f"A_DIFF:\n{a_diff}\nB_DIFF\n{b_diff}")
            prev_commit = commit

        print(commits)

        print(len(changes))
        # remove first commit
        changes = changes[1:]
        print(len(changes))

        return changes


tracker = ChangeTracker()


if __name__ == "__main__":
    tracker.set_actor("OthelloEngineer")
    commits = tracker.get_changes()
    print(commits)
