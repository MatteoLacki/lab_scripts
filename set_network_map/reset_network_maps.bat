rem unset all the network drives
net use I: /delete
net use O: /delete
net use S: /delete
net use T: /delete
net use Z: /delete
net use U: /delete
net use L: /delete
net use X: /delete
net use Y: /delete

rem consistent mapping of drives
net use I: \\msserver\idefix_rawdata
net use O: \\msserver\obelix_rawdata
net use S: \\msserver\synapt
net use T: \\msserver\idefix
net use Z: \\msserver\backup
net use U: \\msserver\users
net use L: \\msserver\legacy
net use X: \\msserver\data
net use Y: \\msserver\symphony

pause