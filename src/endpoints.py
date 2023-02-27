import sys

def generate(link, file):
    """Generate many endpoints from file lines to link
    Ex:
        >>> word = "hello"
        >>> generate("https://example.com/dictionary/{word}/rest/", word)
        >>> https://www.ldoceonline.com/dictionary/hello/rest/
    """
    start = ""
    end = ""

    for index, i in enumerate(link):
        if i == '{':
            end = link[link.index('}')+1:]
            break
        start += i

    with open(file, 'r') as f:
        for i in f.readlines():
            with open(file + '.out.txt', 'a+') as ff:
                data = start + i[:len(i)-1] + end + ',' + i
                ff.write(data)

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
