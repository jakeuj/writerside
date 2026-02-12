# Switch Account

公司跟私人 Github 帳號混用時，會遇到存取公司 repo 但因為認證是私人帳號，導致找不到 repo 的情況

這時可以使用以下方法切換帳號

在 reomte repo 的 url 前加上帳號名稱

```bash
git remote set-url origin https://[username]@github.com/xxx/[repo].git
```

這樣就可以切換帳號了
