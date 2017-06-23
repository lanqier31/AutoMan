# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from Web import web_app

web_app.run(host='0.0.0.0', port=5566)
