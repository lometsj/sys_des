import sys
fd = sys.argv[1]
cmd = sys.argv[2]
temple = "ioctl${cmd}(fd {fd}, cmd const[{cmd}], arg ptr[])".format(fd=fd, cmd=cmd)
print temple
