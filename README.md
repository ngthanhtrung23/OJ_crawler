VOJ_crawler
==========

Crawler for getting my solutions from Vietnam Online Judge [VOJ](https://vn.spoj.com/)

Installation:

```
pip install -r requirements.txt
```


This command will get all your submissions:
   ```
    python crawler/VOJ.py <username> <password>
   ```
   
If you want to get accepted submssions only, please try this command:
   ```
    python crawler/VOJ.py <username> <password> AC_only
   ```

 
Beware of redirected problem, when you enter http://vn.spoj.com/, it maybe redirect to http://www.spoj.com/ sometime. Try add this into your [hosts file](https://en.wikipedia.org/wiki/Hosts_(file)).
```
195.149.199.189 vn.spoj.com
```
Thank [Nguyễn Văn Hoà](https://www.facebook.com/vhnvn) for sharing that.

**If my code get redirected to spoj, it would crawl your submission in SPOJ**
