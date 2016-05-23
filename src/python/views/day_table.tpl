<?xml version="1.0"?>
<html>
<head>
<title>Temperature last 24 hours</title>
</head>
<body>
% import datetime
<table>
% for row in rows:
<tr><td>{{datetime.datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S')}}</td><td>{{row[2]}}</td>
% end
</table>
</body>
</html>
