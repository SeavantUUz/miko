ShoujoA
=========
A static blog written by python . 

**Usage**  
*Be sure your os is Linux.ShoujoA can not run on windows*

* clone it.`git clone git@github.com:SeavantUUz/ShoujoA.git`
* cd and into the ShoujoA
* input `source env/bin/activate`
* edit `config.yaml` by your favorite editor.Revise it to your config.
    * MAIN_PATH is where dirs conpose
    * OUTDIR is a dirname where your htmls be placed
    * BACKUP_DIR is a dirname where your backup dir be placed(Yes,ShoujoA can backup your posts)
    * THEME_DIR is a dirname where the themes be placed
    * All above dirs will be auto create while you run `./shoujo.py --init`.So,don't worry~~
    * NAME is your website name
    * AUTHOR is your name
    * HOMEPAGE is your domin name
    * POSTS_NUM is the number that each page should contain posts
    * DESCRIPTION is your website description
* if you revised.Chmod shoujo.py to 744 and run `./shoujo.py --init`
* write a test file.But remember you should obey some rules.
    * first line is the post's title
    * second line is the archive
    * third line is the tags
    * leave forth line as a blank line
    * the remains line is your post's content
    * ShoujoA will auto find first blank line in content . If found,the former content will be treated as abstrct.
* you can always run `./shoujo.py --post filename` to submit a new post
* you can also run `./shoujo.py --show` to see your posted posts
* run `./shoujo.py --remove index` will delete a post
* run `./shoujo.py --postAll 0` will rebuild all posts from backup dir.Or you can run `./shoujo.py --postAll dirname` to add some posts from dir
* enjoy your ShoujoA!!
* run `./shoujo --updateThemes` to update all themes
* more feathers is on the road.



