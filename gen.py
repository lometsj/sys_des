# -*- coding: utf-8 -*

import os
import sys
import getopt

def gen_ioctl_cmds(driver_name,rt,ioctl):
    ret = []
    with open(rt,'r') as fd:
        buf = fd.read()
        lines = fd.readlines()
        ret.append('#'+ioctl)
        fun_flag = buf.find(ioctl+'(')
        l = buf.find('{',fun_flag)
        flag = 1
        r = l + 1
        while flag != 0 and r<len(buf):
            if buf[r] == '{':
                flag += 1
            if buf[r] == '}':
                flag -= 1
            r += 1

        while buf[l:r].find('\tcase') != -1:
            templ = buf[l:r].find('\tcase')
            tempr = buf[l:r].find(':')
            templ += 6
            if buf[l:r][templ:tempr] == '':
                l += tempr + 1
                continue
            # print (buf[l:r][templ:tempr])
            ret.append( ''.join([
                'ioctl$',
                buf[l:r][templ:tempr],
                '(fd fd_',
                driver_name.replace('_',''), 
                ', cmd const[' , 
                buf[l:r][templ:tempr],
                ']', 
                ', arg ptr[])',
                ]) )
            # (fd fd_sndcompress, cmd const[SNDRV_COMPRESS_SET_PARAMS], arg ptr[in, snd_compr_params])
            l += tempr+1
    return ret


def gen_syzopen_dev(driver_name):
    t = "syz_open_dev${}(dev ptr[in, string[{}]], id intptr, flags flags[open_flags]) {}".format(
        driver_name.replace('_',''),
        "\"/dev/"+driver_name+'\"',
        'fd_'+driver_name.replace('_','')
        )
    return t

def gen_fd(driver_name):
    t = ['resource fd_',driver_name.replace('_',''),'[fd]']
    return ''.join(t)

def gen_head(driver_name,rt):
    t = [
        '#',driver_name,'\n',
        '#',rt,'\n'
    ]

    return ''.join(t)

def gen_txt(driver_name,rt):
    ret = ''
    ret = gen_head(driver_name,rt)
    return ret

def main(argv):
    print argv
    driver_name = ""
    driver_url = ""
    driver_ioctl = ""
    #print argv[1]
    driver_name = argv[0]
    driver_url = argv[1]
    driver_ioctl = argv[2]

    with open('./'+driver_name+'.txt','w') as f:
        f.write(gen_txt(driver_name, driver_url))
        f.write('\n')
        f.write(gen_fd(driver_name))
        f.write('\n')
        f.write(gen_syzopen_dev(driver_name))
        f.write('\n')
        t = gen_ioctl_cmds(driver_name, driver_url, driver_ioctl)
        for j in t:
            f.write(j)
            f.write('\n')            


if __name__=="__main__":
    main(sys.argv[1:])