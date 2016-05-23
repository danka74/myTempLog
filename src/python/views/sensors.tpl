<?xml version="1.0"?>
<html>
<head>
<title>All sensors</title>
</head>
<body>
<table>
% for row in rows:
<tr><td><a href="/last24svg/{{row['id']}}">{{row['id']}}</a></td></tr>
% end
</table>
</body>
</html>
