# alidns
1. Install the python depend
pip install -r requirement.txt

2. fill up config

`cp default.json config.json`

Shange `AccessKeyID` and `AccessKeySecret` to the aliyun keys, and change `Domain' to the prefix of your domain. Such as 'aa' of aa.baidu.com.

3. run

`python alidns`

# more
It may be convenience to run this program periodly, use systemctl or cron etc.
