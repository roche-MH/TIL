# Git

> Git 은 분산버전 관리시스템(DVCS)이다.
>
> 소스코드의 버전 및 이력을 관리할 수 있다.

# 준비하기

윈도우에서 git을 사용하기 위해서 [git bash](https://gitforwindows.org/) 을 설치한다.

git을 활용하기 위해서 GUI 툴인 `source tree`, `github desktop` 등을 활용할 수도 있다.



초기 설치를 완료한 이후에 컴퓨터에 `author` 정보를 입력한다.

이메일 정보를 github에 가입된 이메일로 일치시켜야 커밋 이력들이 관리된다.

```bash
$ git config --global user.name roche-MH
$ git config --global user.email roche5610@gmail.com

```



# 로컬 저장소(repo) 활용하기

## 1. 저장소 초기화

```bash
$ git init
Initialized empty Git repository in C:/Users/student/Desktop/TIL/.git/
(master) 
```

* `.git` 폴더가 생성되며, 여기에 git과 관련된 모든 정보가 저장된다.
* git bash에 `(master)` 라고 표현되는데, 이는 `master`  브랜치에 있다는 뜻이다.



## 2. add

`working diretory` , 즉 작업 공간에서 변경된 사항을 이력으로 저장하기 위해서는 반드시 `staging area` 를 거쳐야 한다.

```bash
$ git add markdown.md # 특정 파일
$ git add images/ # 특정 폴더
$ git add . # 현재 디렉토리
```

* add 전상태

  ```bash
  $ git status
  On branch master
  
  No commits yet
  
  #트래킹 되고 있지 않는 파일들
  # => commit 이력에 한번도 담기지 않은 파일들
  Untracked files:
  #커밋될것에 포함시키려면 git add <file> 을 사용해라
    (use "git add <file>..." to include in what will be committed)
          git.md
          images/
          markdown.md
  
  #아직 커밋될 것들은 없지만
  #untracked file 은 존재한다.
  nothing added to commit but untracked files present (use "git add" to track)
  ```

* `add` 후상태

  ```bash
  $ git add images/
  
  $ git status
  On branch master
  
  No commits yet
  # 커밋될 변화들
  # => staging area 에 있는 파일들
  Changes to be committed:
    (use "git rm --cached <file>..." to unstage)
          new file:   images/image-20191226134152642.png
  
  Untracked files:
    (use "git add <file>..." to include in what will be committed)
          git.md
          markdown.md
  
  $ git add .
  #  . 현재 폴더 모두 add
  ```



## 3.Commit

commit은 이력을 확정짓는 명령어로, 해당 시점의 스냅샷을 기록한다.

커밋시에는 반드시 메세지를 작성 해야하며, 메세지는 변경사항을 알수 있도록 명확하게 작성한다.

```bash
$ git commit -m '마크다운 및 git 정리'
[master (root-commit) 37f9579] 마크다운 및 git 정리
 3 files changed, 114 insertions(+)
 create mode 100644 git.md
 create mode 100644 images/image-20191226134152642.png
 create mode 100644 markdown.md

```

커밋 이후에는 아래의 명령어를 통해 지금까지 작성된 이력을 확인하자.

```bash
$ git log
commit 37f95793c6092d6e7794125e4112e66408fd3d2d (HEAD -> master)
Author: roche-MH <roche5610@gmail.com>
Date:   Thu Dec 26 14:34:57 2019 +0900

    마크다운 및 git 정리
    
$ git log --oneline #한줄로 표시
37f9579 (HEAD -> master) 마크다운 및 git 정리

$ git log -1 ##최근 값 1개
commit 37f95793c6092d6e7794125e4112e66408fd3d2d (HEAD -> master)
Author: roche-MH <roche5610@gmail.com>
Date:   Thu Dec 26 14:34:57 2019 +0900

    마크다운 및 git 정리

```

>  커밋은 해시코드를 바탕으로 구분한다. ex)  37f9759





## 원격저장소(repo) 활용하기

원격 저장소 기능을 제공하는 다양한 서비스 중에 github을 기준으로 설명한다.

### 준비사항

* Gihub에 repository 생성

### 1. 원격저장소 등록

```bash
git remote add origin 깃허브url
```

* 원격저장소 `(remote)` 로 `origin` 이라는 이름으로 `깃허브 url`을 등록 `add` 한다.
* 등록된 원격 저장소 목록을 보기 위해서는 아래의 명령어를 활용한다.

```bash
$ git remote -v
origin  https://github.com/roche-MH/TIL.git (fetch)
origin  https://github.com/roche-MH/TIL.git (push)

```



### 2. `push`  - 원격 저장소 업로드

```bash
$ git push -u origin master
```

`origin` 으로 설정된 원격저장소에 `master` 브랜치로 업로드(`push`)

이후 변경사항이 생길때마다, `add` - `commit`, `push` 를 반복하면 된다.

그리고, 항상 모든 명령어 이후에 연관된 상태를 확인하자

> `status` ,`log`, `remote -v`



## 3. `Pull` - 원격 저장소 에서 받아오기

```bash
$ git pull origin master
```

원격 저장소의 변경 사항을 받아온다.

### 4. `Clone` 

```bash
$ git clone 깃 허브 url
#폴더에 .git (초기화가 안됬을떄 사용)
```

원격저장소를 복제한다.

주의! `init` 명령어와 같이 하자! 