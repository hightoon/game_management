<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>xxx游戏管理系统</title>
  <link rel="stylesheet" type="text/css" href="/static/management_front_end/admin_mngm/css/style.css">
  <script src="/static/management_front_end/js/jQuery.js"></script>

  <!-- More on helper.js in the class -->
  <script src="/static/management_front_end/js/helper.js"></script>
</head>
<body unresolved>
  <div id="main" class="managementpage">
    <div class="row">
      <div id="welcome-bar" class="col-4"><p>您好，admin</p></div>
      <div id="logout-change-password" class="col-4">
        <form action="/logout_change_passwd" method="POST">
          <button name="logout" formaction="/logout">注销</button>&nbsp
          <button name="change_passwd" formaction="/change_passwd">修改密码</button>
        </form>
      </div>
      <div id="general-info-bar" class="col-4"><p>您的店内，今日游戏运行xxx次。</p></div>
      <div id="message-bar" class="col-12"><p>总部新闻：xxxxxx</p></div>
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
      <div id="price-form" class="col-5">
        <h4>价格修改</h4>
        <form action="" method="post">
          <p>
            <label for="shop-name">店名 </label>
            <input id="shop-name" type="text" name="shopname">
          </p>
          <p>
            <label for="host-name">主机 </label>
            <select id="host-name" name="hostname">
              <option value="hosta">主机A</option>
              <option value="hostb" selected>主机B</option>
              <option value="hostc">主机C</option>
            </select>
          </p>
          <p>
            <label for="game-name">游戏 </label>
            <select id="game-name" name="gamename">
              <option value="gamea">游戏A</option>
              <option value="gameb" selected>游戏B</option>
              <option value="gamec">游戏C</option>
            </select>
          </p>
          <input type="submit" value="修改">
        </form>
      </div>
      <div id="price-table" class="col-5">
        <p>this is a price table</p>
      </div>
    </div>
  </div>
  <script src="../js/resumeBuilder.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
