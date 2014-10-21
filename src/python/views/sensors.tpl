<?xml version="1.0"?>
<html>
<head>
<title>All sensors</title>
</head>
<body>
<table>
% for row in rows:
<tr><td>{{row['id']}}</td></tr>
% end
</table>
</body>
</html>
