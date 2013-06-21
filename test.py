def paragraphs(text,is_separator=str.isspace,joiner=''.join):
    paragraph = []
    for line in text:
        if is_separator(line):
            if paragraph:
                yield joiner(paragraph)
                paragraph=[]
        else:
            paragraph.append(line)
    if paragraph:
        yield joiner(paragraph)

f = open('test','r')
f.readline()
f.readline()
text = f.read()
p = paragraphs(text.splitlines(True))
print p
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
print p.next()
f.close()
