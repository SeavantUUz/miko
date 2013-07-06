#!env/bin/python
# coding:utf-8

import argparse
from appleSouffle import post,remove,postAll,show,init,updateThemes,insert,archive,tags

def _parserInput():
    parser = argparse.ArgumentParser(description = 'A static blog engine')
    parser.add_argument("--init",action = "store_true",dest="init",help='init environment')
    parser.add_argument("--show",action = "store_true",dest="show",help='Show all posts you post')
    parser.add_argument("--remove",type=int,dest="remove",help="Remove a node.ex: ./shoujo.py --remove 3")
    parser.add_argument("--insert",nargs = 2,dest="insert",help='insert a post into the list.ex ./shoujo.py --insert filename,index')
    parser.add_argument("--post",nargs='+',dest="post",help="Submit your post.ex: --post=filename")
    parser.add_argument("--postAll",nargs='?',const='default',dest="postAll",help='Rebuild all posts,you can pass a dirname,or notion .Pass 0 to it will set rebuild from backup dir.ex:./shoujo.py --postAll 0 or --postAll=/home/xxx')
    parser.add_argument("--updateThemes",action = "store_true",dest="updateThemes",help='Update all of your themes.Each time you add a new theme and you should run it')
    parser.add_argument("--archive",action="store_true",dest="archive")
    parser.add_argument("--tags",action="store_true",dest="tags")

    args = parser.parse_args()

    return args

def main():
    options = _parserInput()
    if options.init:
        init()
    elif options.insert:
        args = options.insert
        try:
            index = int(args[1])
        except ValueError:
            raise 'please check your input: ./shoujo.py --insert filename index'
        insert(args[0],index)
    elif options.post:
        for post_name in options.post:
            post(post_name)
    elif options.remove != None:
        remove(options.remove)
    elif options.show:
        show()
    elif options.postAll:
        if options.postAll == 'default':
            postAll()
        else:
            postAll(options.postAll)
    elif options.updateThemes:
        updateThemes()
    elif options.archive:
        archive()
    elif options.tags:
        tags()

if __name__ == "__main__":
    main()
