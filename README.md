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

 
Beaware ofredirected problem, when you enter http://vn.spoj.com/, it will redirected to http://www.spoj.com/ sometime. **If my code get redirected to spoj, it would crawl your submission in SPOJ**
   
