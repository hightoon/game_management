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
      <div id="welcome-bar" class="col-4"><p>您好，{{username}}</p></div>
      <div id="logout-change-password" class="col-4">
        <button>注销</button>&nbsp<button>修改密码</button>
      </div>
      <div id="general-info-bar" class="col-4"><p>您的店内，今日游戏运行xxx次。</p></div>
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
      <div id="game-mng" class="col-10">
        <h5 id="host-game-control">游戏控制</h5>
        <div>
          <form action="/game_control" method="POST">
            <p>
              <label for="host-selection">
                <span>主机</span>
                <select name="host-selection">
                  <option value="host1">主机A</option>
                  <option value="host2" selected>主机B</option>
                  <option value="host3">主机C</option>
                </select>
              </label>
              <label for="game-selection">
                <span>游戏</span>
                <select name="game-selection">
                  <option value="game1">火焰飞车</option>
                  <option value="game2" selected>火焰投篮</option>
                  <option value="game3">火焰足球</option>
                </select>
              </label>
            </p>
          </form>
        </div>
        <div>
          <span>控制: </span>
          <button>开始</button>
          <button>重置</button>
        </div>
        <h5 id="host-game-kb-ctrl">游戏控制</h5>
        <div>
          <p>
            <tr>
              <th>主机</th>
              <th>游戏</th>
              <th>状态</th>
              <th>按键接口</th>
              <th>备注</th>
            </tr>
          </p>
        </div>
      </div>
    </div>
  </div>
  <script src="../js/resumeBuilder.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
