#!env/bin/python
# coding:utf-8

import argparse
from shoujo.miko import post,postDir,remove,show,init,themes,aboutme,links#updateThemes,insert,archive,tags,aboutMe,links,feed

def _parserInput():
    parser = argparse.ArgumentParser(description = 'A static blog generator')
    parser.add_argument("--init",action = "store_true",help='init dirs struct')
    parser.add_argument("--show",action = "store_true",help='Show all posts you post')
    parser.add_argument("--remove",help="Remove a node.eg: ./shoujo.py --remove 3")
    parser.add_argument("--post",help="Submit your post.eg: --post filename")
    parser.add_argument("--postDir",help='Submit a dir and all files in the dir will be post.')
    parser.add_argument("--themes",action = "store_true",help='Update all of your themes.Each time you add a new theme and you should run it')
##    parser.add_argument("--archive",action="store_true",dest="archive")
##    parser.add_argument("--tags",action="store_true",dest="tags")
    parser.add_argument("--aboutme",action="store_true",dest="aboutMe")
    parser.add_argument("--links",action="store_true",dest="links")
##    parser.add_argument("--feed",action="store_true",dest="feed")
##
    args = parser.parse_args()

    return args

def main():
    options = _parserInput()
    if options.init:init()
    elif options.post:post(options.post)
    elif options.remove: remove(int(options.remove))
    elif options.show:show()
    elif options.postDir:postDir(options.postDir)
    elif options.themes:themes()
    elif options.aboutMe:aboutme()
    elif options.links:links()
    else:print u'无效参数'
    # elif options.archive:
    #     archive()
    # elif options.tags:
    #     tags()
    # elif options.feed:
    #     feed()

if __name__ == "__main__":
    main()
