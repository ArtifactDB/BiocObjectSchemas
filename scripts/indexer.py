import sys
title = sys.argv[1]
dirpath = sys.argv[2]
gifurl = sys.argv[3]

import os
files = os.listdir(os.path.join(dirpath, "html"))
available = []
for i, x in enumerate(files):
    target = os.path.join(dirpath, "html", x)
    if not os.path.isdir(target):
        continue
    within = os.listdir(target)
    htmls = []
    for y in within:
        if y[-4:] == "html":
            htmls.append("<a href=\"html/" + x + "/" + y + "\">" + y[:-5] + "</a> (<a href=\"raw/" + x + "/" + y[:-5] + ".json" + "\">json</a>)")
    available.append("<li class=\"list-group-item\">" + x + ": " + ', '.join(htmls) + "</li>")

available = "<ul class=\"list-group\">\n" + '\n'.join(available) + "</ul>"

template = """<!DOCTYPE html>
<meta charset="utf-8">
<title>{title}</title>
<html>
<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
</head>
<body class="d-flex flex-column h-100">
    <!-- Begin page content -->
    <main role="main" class="flex-shrink-0">
        <div class="container">
           <div class="jumbotron">
           <h1>{title}</h1>
        </div>
        <div class="container">
          <div class="row align-items-start">
            <div class="col">
           {available} 
            </div>
            <div class="col">
           <img src="{gif}" alt="glomp" class="img-responsive" width="100%" />
        </div>
        </div>
    </main>
</body>
</html>
""".format(title=title, available=available, gif=gifurl)

print(template)
