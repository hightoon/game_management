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
      <div id="general-info-bar" class="col-4"><p>您的店内，今日游戏运行{{tot_game_ops}}次。</p></div>
      <div id="message-bar" class="col-12"><p>总部新闻：xxxxxx</p></div>
    </div>
    <!--div id="message-bar" class="row"><h6>系统消息：xxxxxx</h6></div-->
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
      <div id="user-mng" class="col-10">
        <h4 id="add-new-user">添加用户</h4>
        <form action="/add_user" method="POST">
          <p><strong><abbr title="required">*</abbr></strong>为必填项。</p>
          <p>
            <label for="username">
              <span>用户名: </span>
              <input type="text" id="uname" name="username" required />
              <strong><abbr title="required">*</abbr></strong>
            </label>
          </p>
          <p>
            <label for="password">
              <span>密码: </span>
              <input type="password" id="pass" name="password" required />
              <strong><abbr title="required">*</abbr></strong>
            </label>
          </p>
          <p>
            <label for="email">
              <span>邮箱: </span>
              <input type="email" id="email" name="useremail" required />
              <strong><abbr title="required">*</abbr></strong>
            </label>
          </p>
          <p>
            <label for="name">
              <span>姓名: </span>
              <input type="text" id="name" name="name" />
              <strong><abbr title="required">*</abbr></strong>
            </label>
          </p>
          <p>
            <label for="sex">
              <span>性别:</span>
                <input type="radio" id="male" name="sex" value="male">
                <label for="male">男</label>
                <input type="radio" id="female" name="sex" value="female">
                <label for="female">女</label>
            </label>
          </p>
          <input type="submit" value="添加" />
        </form>
        <h4 id="delete-user">删除用户</h4>
        <form action="delete_user" method="POST">
          <p>
            <label for="username">
              <span>用户名: </span>
              <input type="text" id="uname" name="username" required />
              <strong><abbr title="required">*</abbr></strong>
            </label>
          </p>
          <input type="submit" value="删除" />
        </form>
      </div>
    </div>
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
