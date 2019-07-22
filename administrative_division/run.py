# -*- coding: utf-8 -*-

import os

from scrapy import cmdline


def main():
    dist_path = os.path.join(os.getcwd(), os.path.pardir, 'dist')
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    name = 'zx_adm_spider'
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())


if __name__ == '__main__':
    main()
