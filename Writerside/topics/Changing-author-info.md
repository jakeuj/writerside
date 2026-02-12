# Changing author info

於 Windows 修改全部已 Commit & Push 的 History 中的 Author 資訊。

## 修改全部 Commit 的 Author 資訊

1. 打開 Git Bash.

![git-bash.png](git-bash.png){style="block"}

1. Clone Repository.

```bash
git clone --bare https://hostname/user/repo.git
cd repo.git
```

1. 複製腳本並取代以下的變數
    - OLD_EMAIL: 舊的 Email
    - CORRECT_NAME: 正確的名字
    - CORRECT_EMAIL: 正確的 Email

```bash
#!/bin/sh

git filter-branch --env-filter '

OLD_EMAIL="your-old-email@example.com"
CORRECT_NAME="Your Correct Name"
CORRECT_EMAIL="your-correct-email@example.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
export GIT_COMMITTER_NAME="$CORRECT_NAME"
export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
export GIT_AUTHOR_NAME="$CORRECT_NAME"
export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
```

1. 複製修改後的腳本並貼到 git bash 中執行腳本
2. 確認新的紀錄是否正確

```Bash
git log --pretty=format:"%h - %an <%ae>"
```

1. Push 到遠端 Repository

```bash
git push --force --tags origin 'refs/heads/*'
```

1. 刪除本地的 Clone Repository

```bash
cd ..
rm -rf repo.git
```

## 參考資料

- [Changing author info](https://docs.github.com/en/enterprise/2.17/user/github/using-git/changing-author-info)
