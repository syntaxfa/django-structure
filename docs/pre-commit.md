### Pre commit

## for install dependencies:
```shell
pre-commit clean
&&
pre-commit install
&&
pre-commit install --hook-type commit-msg
```

## for applying new added rule:
```shell
pre-commit clean &&
pre-commit install Or pre-commit install --hook-type commit-msg
```

## running pre-commit for test
```shell
pre-commit run --all-files
```

## testing gitlint
```shell
echo "bad commit message" > test_commit_msg.txt
&&
gitlint --msg-filename test_commit_msg.txt
```

## Or:
```shell
pre-commit run gitlint --hook-stage commit-msg --commit-msg-filename .git/COMMIT_EDITMSG
```
