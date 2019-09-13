def main():
    s = 'http://quotes.toscrape.com/page/1/'
    print(s.split('/'))
    print(s.split('/')[-1])
    print(s.split('/')[-2])


if __name__ == "__main__":
    main()