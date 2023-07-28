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

**Please Note:** If you get warnings like the following, you can safely ignore them:

> PHP Warning:  mkdir(): File exists in /root/cherrytreetomarkdown/src/logic/CherryToMD.php on line 24

## Recommendation: Automatically Split CherryTree Knowledge Base Into Individual Files

As of 2023-07-28, the conversion tool provided at <https://gitlab.com/kibley/cherrytreetomarkdown> does not support splitting the input file into multiple output files; all content of your CherryTree knowledge base will be written to a single `index.md` file.

If you have a large knowledge base (maybe even sorted in a hierarchical fashion), this is not ideal.
To circumvent this limitation, we've added the script `splitconvert.py`, which first splits a CherryTree XML file into individual nodes and then uses the original conversion tool to convert each of these nodes to Markdown. While there are some file movement and renaming tasks involved, the whole process is fully transparent to the user and all you'll see are the final Markdown files — sorted into folders just like you had them in CherryTree.

You can use this more advanced version of the conversion process as shown below.

~~~ bash
$ docker run --rm -it --name cherry2md -v "${PWD}:/root/cherrytreetomarkdown/volumes/input" -v "${PWD}:/root/cherrytreetomarkdown/volumes/output" cherry2md

root@a32456004b2f:~/cherrytreetomarkdown# ./splitconvert.py -i volumes/input/MyCherryTreeKnowledgeBase.ctd -o volumes/output/MyConvertedKnowledgeBase
[*] Starting node to individual file conversion.
[*] Node to file conversion: All done.
[*] Starting XML to Markdown conversion.
PHP Warning:  mkdir(): File exists in /root/cherrytreetomarkdown/src/logic/CherryToMD.php on line 24
[...]
[*] XML to Markdown conversion: All done.
[*] Fixing image and file paths ...
[*] Fixed image and file paths!
~~~

~~~ bash
root@a32456004b2f:~/cherrytreetomarkdown# ./splitconvert.py -h
usage: splitconvert.py [-h] [-v] -i INPUT [-o OUTPUT] [-k]

options:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -i INPUT, --input INPUT
                        A single CherryTree input file in *.ctd format
  -o OUTPUT, --output OUTPUT
                        Output directory to write split files to (defaults to current directory)
  -k, --keep            Keeps all of the individual CherryTree node files instead of deleting them after conversion to Markdown
~~~
