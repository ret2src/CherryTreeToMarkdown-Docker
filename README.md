# Docker Wrapper for CherryTreeToMarkdown

This is a quick and dirty Docker wrapper for [CherryTreeToMarkdown](https://gitlab.com/kibley/cherrytreetomarkdown).
It allows you to convert your CherryTree files to Markdown without installing all the dependencies on your host.

## Installation

~~~ bash
$ git clone https://github.com/ret2src/CherryTreeToMarkdown-Docker
$ cd CherryTreeToMarkdown-Docker
$ docker build -t cherry2md .
~~~

## Usage

~~~ bash
$ ls -alh input/
total 272K
drwxr-xr-x 2 user user 4.0K Jul 25 14:58 .
drwxr-xr-x 4 user user 4.0K Jul 25 15:01 ..
-rw-r--r-- 1 user user 264K Jul 25 14:58 MyCherryTreeNotes.ctd

$ ls -alh output/
total 168K
drwxr-xr-x 4 user user 4.0K Jul 25 14:58 .
drwxr-xr-x 4 user user 4.0K Jul 25 15:01 ..

$ docker run --rm -it --name cherry2md -v "${PWD}/input:/root/cherrytreetomarkdown/volumes/input" -v "${PWD}/output:/root/cherrytreetomarkdown/volumes/output" cherry2md

root@76eaa5863875:~/cherrytreetomarkdown# php cherrytomd.php ./volumes/input/MyCherryTreeNotes.ctd ./volumes/output/MyCherryTreeNotes/

$ ls -alh output/MyCherryTreeNotes/
total 168K
drwxr-xr-x 4 root root 4.0K Jul 25 15:11 .
drwxr-xr-x 5 user user 4.0K Jul 25 15:11 ..
drwxr-xr-x 2 root root 4.0K Jul 25 15:11 files
drwxr-xr-x 2 root root 4.0K Jul 25 15:11 images
-rw-r--r-- 1 root root 151K Jul 25 15:11 index.md
~~~

**Please Note:** Always make sure to define a new subdirectory for your output, otherwise you'll run into errors like:

> PHP Warning:  mkdir(): File exists in /root/cherrytreetomarkdown/src/logic/CherryToMD.php on line 24
