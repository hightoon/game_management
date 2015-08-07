<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>游戏管理系统</title>
  <link rel="stylesheet" type="text/css" href="/static/management_front_end/admin_mngm/css/style.css">
  <script src="/static/management_front_end/js/jQuery.js"></script>

  <!-- More on helper.js in the class -->
  <script src="/static/management_front_end/js/helper.js"></script>
</head>
<body unresolved>
  <div id="main" class="managementpage">
    <div class="row">
      <div id="welcome-bar" class="col-4"><p>
        您好，<a href="/index/{{username}}">{{username}}</a>
      </p></div>
      <div id="logout-change-password" class="col-4">
        <form action="/logout_change_passwd" method="POST">
          <button name="logout" formaction="/logout">注销</button>&nbsp
          <button name="change_passwd" formaction="/change_passwd">修改密码</button>
        </form>
      </div>
      <div id="general-info-bar" class="col-4">
        <p>
          %if is_admin:
            您的店内，今日游戏运行{{tot_game_ops}}次。
          %else:
            您今日运行游戏{{num_of_ops}}次！
          %end
        </p>
      </div>
      <div id="message-bar" class="col-12"><p>总部新闻：{{news_title}}</p></div>
    </div>
    <!--div id="message-bar" class="row"><h6>系统消息：xxxxxx</h6></div-->
    <div class="row">
      <div class="col-2">
        <ul class="block-list">
          %if is_admin:
            <li><h4><a href="/usermng">用户管理</a></h4></li>
          %end
          <li><h4><a href="/gamemng">游戏管理</a></h4></li>
          %if is_admin:
          <li><h4><a href="/pricingmng">价格管理</a></h4></li>
          <li><h4><a href="/statistics">数据统计</a></h4></li>
          %end
          <li><h4><a href="/notification">消息通知</a></h4></li>
          <li><h4><a href="/logout">退出登录</a></h4></li>
        </ul>
      </div>
      <div id="game-stat" class="col-10">
        <div id="stat-config-form" class="col-9">
          <form id="stat-conf" name="stat-conf" action="/statistics" method="POST">
            <p>
              <label for="period">
                <span>时间</span>
                <select name="period">
                  <option value="1">最近1天</option>
                  <option value="7">最近7天</option>
                  <option value="30">最近30天</option>
                  <option value="50">最近50天</option>
                </select>
              </label>
              <label for="order">
                <span>排序方式</span>
                <select name="order">
                  <option value="price">价格</option>
                  <option value="timestamp">时间</option>
                  <option value="game">游戏</option>
                  <option value="host">从机</option>
                </select>
              </label>
              <button type="submit" form="stat-conf" name="submit" value="go">确定</button>
            </p>
          </form>
        </div>
        <table class="game-stat-table">
          <tbody>
            <tr>
              <th>主机</th>
              <th>游戏</th>
              <th>店员</th>
              <th>次数</th>
              <th>是否上报</th>
            </tr>
            %for gminfo in gminfolist:
              <tr>
                <td>{{gminfo[1]}}</td>
                <td>{{gminfo[2]}}</td>
                <td>{{gminfo[0]}}</td>
                <td>{{gminfo[3]}}</td>
                <td>{{gminfo[4]}}</td>
              </tr>
            %end
          </tbody>
        </table>
        <h4>详细报表</h4>
        <table class="detail-game-stat">
          <tbody>
            <tr>
              <th>主机</th>
              <th>游戏</th>
              <th>价格</th>
              <th>时间</th>
              <th>店员</th>
              <th>是否上报</th>
              <th>店名</th>
              <th>区域</th>
            </tr>
            %for detail in detailed_game_info:
              <tr>
                <td>{{detail[1]}}</td>
                <td>{{detail[2]}}</td>
                <td>{{detail[3]}}</td>
                <td>{{detail[4]}}</td>
                <td>{{detail[0]}}</td>
                <td>{{detail[5]}}</td>
                <td>梦幻谷</td>
                <td>杭州</td>
              </tr>
            %end
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
