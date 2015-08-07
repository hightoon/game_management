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
      <div id="general-info-bar" class="col-4"><p>您的店内，今日游戏运行{{tot_game_ops}}次。</p></div>
      <div id="message-bar" class="col-12"><p>总部新闻：{{news_title}}</p></div>
    </div>
    <div class="row">
      <div class="col-2">
        <ul class="block-list">
          %if is_admin:
            <li><h4><a href="/usermng">用户管理</a></h4></li>
          %end
          <li><h4><a href="/gamemng">游戏管理</a></h4></li>
          <li><h4><a href="/pricingmng">价格管理</a></h4></li>
          <li><h4><a href="/statistics">数据统计</a></h4></li>
          <li><h4><a href="/notification">消息通知</a></h4></li>
          <li><h4><a href="/logout">退出登录</a></h4></li>
        </ul>
      </div>
      <div class="col-10">
        <div id="price-form" class="col-5">
          <h4>价格修改</h4>
          <form action="/change_price" method="post">
            <p>
              <label for="shop-name">店名 </label>
              <input id="shop-name" type="text" name="shopname" placeholder="可不填">
            </p>
            <p>
              <label for="host-name">主机 </label>
              <select id="host-name" name="hostname">
                %for host in hosts:
                  <option value="{{host[0]}}" selected>{{host[0]}}</option>
                %end
                <!--option value="default" selected>请选择</option-->
              </select>
            </p>
            <p>
              <label for="game-name">游戏 </label>
              <select id="game-name" name="gamename">
                %for game in games:
                  <option value="{{game[0]}}" selected>{{game[0]}}</option>
                %end
                <!--option value="default" selected>请选择</option-->
              </select>
            </p>
            <p>
              <label for="timing">时间 </label>
              <input id="timing" type="text" name="gametiming" placeholder="例如: 13:00-15:00">
            </p>
            <p>
              <label for="price-range">价格 </label>
              <input id="price-range" type="text" name="price" placeholder="最低20">
            </p>
            <input type="submit" value="修改">
          </form>
        </div>
        <div id="price-list-page" class="col-8">
          <h4>价格列表</h4>
          <table class="price-list">
            <tr>
              <th>主机</th>
              <th>游戏</th>
              <th>价格</th>
              <th>时间区间</th>
            </tr>
            %for price in price_list:
              <tr>
                <td>{{price[0]}}</td>
                <td>{{price[1]}}</td>
                <td>{{price[2]}} </td>
                <td>{{price[3]}}</td>
              </tr>
            %end
          </table>
        </div>
      </div>
    </div>
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
