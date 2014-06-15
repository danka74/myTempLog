<?xml version="1.0"?>
<html>
<head>
<title>Temperature last 24 hours</title>
</head>
<body>
<table>
% for row in rows:
<tr><td>{{row['timestamp']}}</td><td>{{row['value']}}</td>
% end
</table>
</body>
</html>