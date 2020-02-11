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