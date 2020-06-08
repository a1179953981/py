#!/usr/bin/env python3
#
#
#

import re

domain_list ="""
server {
    listen 80;
    server_name h.eee.com
    h.scrjak.xin
    h8-uat.ihuayou.com
    h8.ccc-32.com
    ccc-r.scrjak.xin
    uat-cds.eee.com;
    
    location / {
        root /data/wwwroot/ihuayou.com;
    }
    access_log pheonix.com.log;"
}
"""

# re_str=re.compile()
result=re.findall('server_name \w+\.\w+\.\w+\s?\n+', domain_list)
print(result)
