

# Baidu-tieba-university
Used python2 for this project.
Collect Baidu-tieba university infoamtion for practice.
<br>
## Function Introduce
### 1. Get_university_list.py
  从 http://gkcx.eol.cn 上获取大学的列表。
  <br>
### 2. Filter_university_with_tieba_web.py.py
  筛选出有对应贴吧的大学名称。
  <br>
### 3. Collect_university_tieba_info.py
  采集大学贴吧的发帖数量以及会员人数，存入本地的csv文件并分析。
  <br>
### 4. Collect_tieba_items_title_to_file.py
  采集大学贴吧前五页主题帖的标题/作者/回复数量等信息，并按文件夹分类存到本地。
  <br>
### 5. Collect_tieba_items_title_to_MySQL.py
  采集大学贴吧前五页主题帖的标题/作者/回复数量等信息，存入MySQL数据库。
  <br>
  

# Data Analysis
### 1.百度贴吧本科大学贴吧会员人数(万)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧会员人数(万).png)
三峡大学贴吧会员人数最多，为113W。然后是清华北大川大等校，会员数量约为50W。
<br>
### 2.百度贴吧本科大学贴吧总回复贴数量(万)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧总回复贴数量(万).png)
<br>
### 3.百度贴吧本科大学贴吧总主题帖数量(万)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧总主题帖数量(万).png)
在总回复数和发主题贴数量来看，三峡清华北大武大会员人数多，但贴吧活跃度不高。
<br>
### 4.百度贴吧本科大学贴吧人均发回复贴数量(条)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧人均发回复贴数量(条).png)
<br>
### 5.百度贴吧本科大学贴吧人均发主题数量(条)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧人均发主题数量(条).png)
从人均发主题帖数量来看，最多的是福建工程学员，每个会员平均为吧里贡献了约3条主题贴。
<br>
### 6.百度贴吧本科大学贴吧每贴平均回复数量(条)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/百度贴吧本科大学贴吧每贴平均回复数量(条).png)
<br>

### 7.会员人数&活跃度
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/会员人数&活跃度.png)
关于会员人数与发帖&回复积极性的关系，三峡大学会员数量太多，几乎快是第二名两倍，我们排除三峡大学这个个例重新作图。
### 8.会员人数&活跃度(排除最大值三峡大学)
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/会员人数&活跃度(排除最大值三峡大学).png)
总的趋势是：
<br>1.主题帖/回复贴与会员人数成正比（除了北大清华三峡，会员众多，但很少发言）。
<br>2.人均发主题数量趋势较平稳，在0.5~1.5之间，中间段趋近于1（可以说具有一人一贴的特点，说明大部分人是有一定的需求（咨询，交流）后加入的贴吧）。
<br>3.人均回复贴数量集中在35条。
<br>4.每贴平均回复数量在会员人数超过5W后，曲线较为平稳，均值为每个主题帖约有27条回复（会员人数达到一定规模后，建立起社区生态）。
<br>
### 9.会员人数与发言情况的散点图
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/会员人数与发言情况的散点图.png)
<br>
### 10.主题吸引程度的散点图
![image](https://github.com/nickliqian/Baidu-tieba-university/blob/master/Analysis%20Chart/主题吸引程度的散点图.png)
>随着会员人均发主题帖数的增长，每个帖子的回复数是增长的，在人均发帖数达到1的时候，每个帖子回复数开始下降（水贴太多，不想回复）。
