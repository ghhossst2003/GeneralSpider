# GeneralSpider
A genenal spider base on Scrapy. It crawl web page from a website and save it, than you can use them to do anything. so this spider force on how to crawl web page.

一个基于Scrapy的通用爬虫。爬取页面并保存，以便于后续进行任何操作，所以这个爬虫主要集中解决怎么去爬取网页的问题。

# install Scrapy
1 update the pip3 to lastest
2 pip3 install scrapy
It is posible you need to install Rust on your compute.

how to install Rust:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Create project on scrapy
scrapy startproject <name> [dir]
name: project name
dir: project dir

# Generate a spider on the project
scrapy genspider [options] <name> <domain>


# Start the Spider
scrapy crawl [spider name] -s JOBDIR=<dir>

example:
scrapy crawl yahoo -s JOBDIR=jobs/001

# Stop the Spider 
two times of Ctrl+c
