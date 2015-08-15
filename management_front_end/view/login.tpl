<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>游戏管理系统</title>
  <link rel="stylesheet" type="text/css" href="/static/management_front_end/bsfiles/css/bootstrap.css">
  <link rel="stylesheet" type="text/css" href="/static/management_front_end/admin_mngm/css/style.css">
  <script src="/static/management_front_end/js/jQuery.js"></script>

  <!-- More on helper.js in the class -->
  <script src="/static/management_front_end/js/helper.js"></script>
</head>
<body unresolved>
  <div class="login-container">
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4" id="login-form">
        <form class="form-signin" action="/login" method="POST">
          <input type="text" name="username" class="login-user" placeholder="用户名" required autofocus>
          <br/><br/><br/>
          <input type="password" name="password" class="login-user" placeholder="密码">
          <br/><br/><br/>
          <button class="btn btn-xl btn-warning btn-block" id="login-but" type="submit">
            登录
          </button>
          <br/>
          <input class="fgt-passwd" type="submit" name="forget_passwd" value="忘记密码?" />
        </form>
      </div>
      <div class="col-4"></div>
      <br/><br/><br/>
    </div>
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
