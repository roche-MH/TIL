# Web

```python
<form action="http://127.0.0.1" >
    
    <input type=text name=id>   텍스트박스
    <input type=submit value="send">  버튼
    
</form>
```

![image-20200211103911235](C:\Users\Student\Desktop\typora\image\image-20200211103911235.png)

```pyhton
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 80))
server_socket.listen(0)
print("listening")
client_socket, addr = server_socket.accept()
print("accepting")
data = client_socket.recv(65535)

print("receive: "+ data.decode())

client_socket.close()
-----------------------------
listening
accepting
receive: GET /?id=hello HTTP/1.1          ### id = hello
Host: 127.0.0.1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36
Sec-Fetch-Dest: document
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
```



## 브라우저 요청시 특정 글자 출력

```python
#simple http server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 80))
server_socket.listen(0)
print("listening")
client_socket, addr = server_socket.accept()
print("accepting")
data = client_socket.recv(65535)

print("receive: "+ data.decode())
client_socket.send('HTTP/1.0 200 OK\r\n\r\nHello'.encode('utf-8')) # 형식
#send 형식 byte 형식으로 바꿔주기 위해 encode('utf-8')
client_socket.close()

#색상 입히기
client_socket.send('HTTP/1.0 200 OK\r\n\r\n<font color=red>Hello</font>'.encode('utf-8')) #send 형식


----------------------------------------------------------------------------------

listening
accepting
receive: GET /fefefe HTTP/1.1
Host: 127.0.0.1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36
Sec-Fetch-Dest: document
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
```

![image-20200211105058418](C:\Users\Student\Desktop\typora\image\image-20200211105058418.png)

![image-20200211105212050](C:\Users\Student\Desktop\typora\image\image-20200211105212050.png)



### 시간 표출하기

```python
from datetime import datetime
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 80))
server_socket.listen(0)
print("listening")
while True:
    client_socket, addr = server_socket.accept()
    print("accepting")
    data = client_socket.recv(65535)
    
    print("receive: "+ data.decode())
    header = 'HTTP/1.0 200 OK\r\n\r\n' #send 형식
    html = 'hello' + str(datetime.now())
    client_socket.send(header.encode('utf-8'))
    client_socket.send(html.encode('utf-8'))
    client_socket.close()
```

![image-20200211112022236](C:\Users\Student\Desktop\typora\image\image-20200211112022236.png)

### 웹서버로 호출된 명령어 확인

```python
#simple http server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 80))
server_socket.listen(0)
print("listening")
client_socket, addr = server_socket.accept()
print("accepting")
data = client_socket.recv(65535)
data = data.decode()
headers = data.split("\r\n")
print(headers[0])   # 첫번째 줄 출력
print(headers[0].split(" ")[1]) # 스페이스로 나눈뒤 1번째 리스트

#print("receive: "+ data.decode())
client_socket.send('HTTP/1.0 200 OK\r\n\r\n<font color=red>Hello</font>'.encode('utf-8')) #send 형식

client_socket.close()
--------------------------------------------------------------------------
listening
accepting
GET /index.html HTTP/1.1
/index.html
```

### 이미지파일 띄우기

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 80))
server_socket.listen(0)
print("listening")

while True :
    client_socket, addr = server_socket.accept()
    print("accepting")
    data = client_socket.recv(65535)    
    data = data.decode()
    #ext = extractext(filename)
    
    #if '.html' in ['.jpg','jpeg','.png']
    
    headers = data.split("\r\n")
    filename = headers[0].split(" ")[1]
   
    if '.html' in filename:
        file = open("."+ filename, 'rt', encoding='utf-8') ##t = text , char
        html = file.read()
        header = 'HTTP/1.0 200 OK\r\n\r\n'    
    
        client_socket.send(header.encode("utf-8"))
        client_socket.send(html.encode("utf-8"))
        client_socket.close()
    elif '.png' in filename:
        client_socket.send('HTTP/1.1 OK\r\n'.encode())
        client_socket.send('Content-Type: image/png\r\n'.encode())    
        client_socket.send('Accept-Ranges: bytes\r\n\r\n'.encode()) ##마지막은 \r\n\r\n 두번 해야되고 
        file = open("."+ filename, 'rb') # b = binary , img
        client_socket.send(file.read())
        file.close()
        
    else:
        header = 'HTTP/1.0 404 File Not Found\r\n\r\n'
        client_socket.send(header.encode('utf-8'))
    client_socket.close()    
    
```



![image-20200211134525286](C:\Users\Student\Desktop\typora\image\image-20200211134525286.png)

### 아이콘, index.html 만들어서 적용하기

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 81))
server_socket.listen(0)
print("listening")

while True :
    client_socket, addr = server_socket.accept()
    print("accepting")
    data = client_socket.recv(65535)    
    data = data.decode()
    print(data)
    
    try:
        #ext = extractext(filename)
    
        #if '.html' in ['.jpg','jpeg','.png']
        headers = data.split("\r\n")
        filename = headers[0].split(" ")[1]
    
   
        if '.html' in filename:

            file = open("."+ filename, 'rt', encoding='utf-8') ##t = text , char
            html = file.read()
            header = 'HTTP/1.0 200 OK\r\n\r\n'    
        
            client_socket.send(header.encode("utf-8"))
            client_socket.send(html.encode("utf-8"))
            client_socket.close()
        elif '.png' in filename or '.ico' in filename:
            client_socket.send('HTTP/1.1 OK\r\n'.encode())
            client_socket.send('Content-Type: image/png\r\n'.encode())    
            client_socket.send('Accept-Ranges: bytes\r\n\r\n'.encode())
            file = open("."+ filename, 'rb') # b = binary , img
            client_socket.send(file.read())
            file.close()
        
        else:
            header = 'HTTP/1.0 404 File Not Found\r\n\r\n'
            client_socket.send(header.encode('utf-8'))
    except Exception as e:
        print(e)
    client_socket.close()    
```

![image-20200211135732593](C:\Users\Student\Desktop\typora\image\image-20200211135732593.png)

폴더 내 favicon.ico 파일이랑 index.html, image.png 가 필요함

```html
<!DOCTYPE html>
    <img src="image.png" >
    <br>
    <input type =text name=id>
    <input type = submit value="send">
    <font color=blue> hi hi </font>
</html>
```



### ServerSide program

```python
import subprocess #특정 어플리케이션을 실행할수 있음

output = subprocess.check_output(['python.exe','test.py']) [#실행, 파라미터] ex) consol> python test.py
print(output)
print(type(output))
print(type(output.decode('cp949')))   #test.py에 한글 파일이 들어가서 cp949 로 인코딩 해주어야 한다.
print(output.decode('cp949'))
    ---------------------------------------
b'a+b \xb4\xc2 20\r\n'
<class 'bytes'>
<class 'str'>
a+b 는 20
```



### 응용해서 웹 호출시 프로그램 실행

```python
import subprocess
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 83))
server_socket.listen(0)
print("listening")

while True :
    client_socket, addr = server_socket.accept()
    print("accepting")
    data = client_socket.recv(65535)    
    data = data.decode()
    print(data)
    
    try:
        #ext = extractext(filename)
    
        #if '.html' in ['.jpg','jpeg','.png']
        headers = data.split("\r\n")
        filename = headers[0].split(" ")[1]
        if '.py' in filename:
            header = 'HTTP/1.0 200 OK\r\n\r\n' 
            output = subprocess.check_output(['python.exe',"."+filename])
            html = output.decode('cp949')
            client_socket.send(header.encode("cp949"))
            client_socket.send(html.encode("cp949"))
            
        elif '.html' in filename:

            file = open("."+ filename, 'rt', encoding='utf-8') ##t = text , char
            html = file.read()
            header = 'HTTP/1.0 200 OK\r\n\r\n'    
        
            client_socket.send(header.encode("utf-8"))
            client_socket.send(html.encode("utf-8"))
            client_socket.close()
        elif '.png' in filename or '.ico' in filename:
            client_socket.send('HTTP/1.1 OK\r\n'.encode())
            client_socket.send('Content-Type: image/png\r\n'.encode())    
            client_socket.send('Accept-Ranges: bytes\r\n\r\n'.encode())
            file = open("."+ filename, 'rb') # b = binary , img
            client_socket.send(file.read())
            file.close()
        
        else:
            header = 'HTTP/1.0 404 File Not Found\r\n\r\n'
            client_socket.send(header.encode('utf-8'))
    except Exception as e:
        print(e)
    client_socket.close()
```

![image-20200211144113273](C:\Users\Student\Desktop\typora\image\image-20200211144113273.png)

### python 코드에 html 넣어서 웹으로 출력하기

```python
test.py
--------
html = """

<html>
    <head>
        <meta charset = "cp949">
    </head>
    <body>
        <img src="image.png" >
    <br>
        <font color=red>이미지 글자</font>
        <input type =text name=id>
        <input type = submit value="확인">
    <br>
        쿠폰번호 입력
        <input type = text name =id1>
        <input type = submit value="입력">
    <br>
        아이디 <input type = text name =id2> 이메일 <input type = text name =id3>
        <input type = submit value="신고하기">
    </body>
</html>
"""

print(html)
```

#### Server code는 위와 동일하고 , 출력물

![image-20200211150043959](C:\Users\Student\Desktop\typora\image\image-20200211150043959.png)



### template 개념으로 html 짜기

```python
html = """
<html>
    <head>
        <meta charset = 'utf-8'>
    </head>

    <body>
        <font color=red> @out</font>
    <table border=1>
        <tr>
            <td>이름</td> <td>@name</td>
        </tr>
        <tr>
            <td>email</td> <td>@email</td>
        </tr>
    </table>

     </body>
</html>
"""


html = html.replace("@out","제목출력")
html = html.replace("@out","이순신")
html = html.replace("@out","lee@gmail.com")
print(html)
```

![image-20200211162403162](C:\Users\Student\Desktop\typora\image\image-20200211162403162.png)

### 간단 예제

```python
html = "hello @v1        test @v2      item @v3"

html = html.replace("@v1","안녕하세요")
html = html.replace("@v2","이순신")
html = html.replace("@v3","^^")
print(html)
----------------------------------------
hello 안녕하세요        test 이순신      item ^^

--------------------- 함수 구현 ----------
def render(html,data):
    for key,value in data.items():
        html= html.replace("@"+key,value)
    return html
        
html = "hello @v1        test @v2      item @v3"
data = {"v1":"안녕하세요", "v2":"이순신","v3":"^^"}
html = render(html,data)
print(html)
-----------------------------------------
hello 안녕하세요        test 이순신      item ^^

-----------------------------------------
def renderfile(file,data):
    html = open(file, "rt", encoding='utf-8')
    for key,value in data.items():
        html= html.replace("@"+key,value)
    return html

data = {"title":"나의 홈페이지", "name":"홍길동","email":"^^"}
print(renderfile("templat.html",data))
-----------------------------------------
hello 안녕하세요        test 이순신      item ^^
```

