<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>xxx游戏管理系统</title>
  <link rel="stylesheet" type="text/css" href="/static/management_front_end/usr_mgr/css/style.css">
  <script src="../js/jQuery.js"></script>

  <!-- More on helper.js in the class -->
  <script src="../js/helper.js"></script>
</head>
<body unresolved>
  <div id="main" class="managementpage">
    <div class="row">
      <div class="col-12"><h2>游戏管理系统</h2></div>
    </div>
    <div class="row">
      <div class="col-2">
        <ul class="block-list">
          <li><h4><a href="index.html">游戏管理</a></h4></li>
          <li><h4><a>时间费用</a></h4></li>
          <li><h4>生成报告</h4></li>
          <li><h4><a href="/logout">退出登录</a></h4></li>
        </ul>
      </div>
      <div id="game-table" class="col-10">
        <table id="game-hosts-table" class="host-game-table">
          <tr>
            <th>从机名</th>
            <th>从机地址</th>
            <th>游戏</th>
            <th>状态</th>
          </tr>
            %for game in games:
              <tr>
                %for item in game:
                  <td>{{item}}</td>
                %end
              </tr>
            %end
        </table>
      </div>
    </div>
  </div>
  <script src="../js/resumeBuilder.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
