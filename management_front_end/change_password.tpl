
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>修改登录密码</title>

    <!-- Bootstrap core CSS -->
    <link href="../../dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/management_front_end/chngpass.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="../../assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <div class="container">
      <div class="row">
        <div class="col-12">
          <h2 class="signin-page-heading">修改登录密码</h2>
        </div>
      </div>
      <form class="form-signin" action="/change_password" method="POST">
        <!--h3 class="form-signin-heading">请登录</h3-->
        <!--label for="inputEmail" class="sr-only">用户名</label-->
        <input type="text" name="username" class="form-control" placeholder="用户名" required autofocus>
        <!--label for="inputPassword" class="sr-only">密码</label-->
        <input type="password" name="password_new" class="form-control" placeholder="新密码" autofocus>
        <input type="password" name="password_confirm" class="form-control" placeholder="确认密码" autofocus>
        <div class="checkbox">
          <!--label>
            <input type="checkbox" value="remember-me"> 记住我
          </label-->
          <button class="btn btn-lg btn-primary btn-block" type="submit">确定修改</button>
          <!--a href="/forget_password">忘记密码</a-->
        </div>
        <!--button class="btn btn-lg btn-primary btn-block" type="submit">登录</button-->
      </form>

    </div> <!-- /container -->


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
