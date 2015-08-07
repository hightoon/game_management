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
<body>
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
    <!--div class="row"-->
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
      <div class="col-10">
        <p>
          截至止{{nowtime}}, 今日：<br/>
          %if is_admin:
            <ul>
              %for ui in usrinfo:
                <li>{{ui[0]}}运行游戏{{ui[1]}}次，登录时间{{ui[2]}}！</li>
              %end
            </ul>
          %else:
            <ul><li>您已经运行游戏{{num_of_ops}}次。</li></ul>
          %end
        </p>
      </div>
    <!--/div-->
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
</body>
</html>
