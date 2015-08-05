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
          %if is_admin:
          <li><h4><a href="/pricingmng">价格管理</a></h4></li>
          <li><h4><a href="/statistics">数据统计</a></h4></li>
          %end
          <li><h4><a href="/notification">消息通知</a></h4></li>
          <li><h4><a href="/logout">退出登录</a></h4></li>
        </ul>
      </div>
      <div id="game-mng" class="col-10">
        <h5 id="host-game-control">游戏控制</h5>
        <div class="row">
          <form id="start-game-form" action="/game_control" method="POST">
            <p>
              <label for="host">
                <span>主机</span>
                <select name="host">
                  %for host in hosts:
                    <option value="{{host[1]}}" selected>{{host[0]}}</option>
                  %end
                  <option value="default" selected>请选择</option>
                    <!--option value="host1">主机A</option>
                    <option value="host2" selected>主机B</option>
                    <option value="host3">主机C</option-->
                </select>
              </label>
              <label for="game">
                <span>游戏</span>
                <select name="game">
                  %for game in games:
                  <option value="{{game[1]}}" selected>{{game[0]}}</option>
                  %end
                  <option value="default" selected>请选择</option>
                  <!--option value="game1">火焰飞车</option>
                  <option value="game2" selected>火焰投篮</option>
                  <option value="game3">火焰足球</option-->
                </select>
              </label>
            </p>
          </form>
        </div>
        <div class="row">
          <span>控制 </span>
          <button type="submit" form="start-game-form" name="op" value="start">开始</button>
          <button type="submit" form="start-game-form" name="op" value="reset">重置</button>
          <button type="submit" form="start-game-form" name="op" value="stop">停止</button>
        </div>
        <h5 id="host-game-kb-ctrl">游戏控制(键盘)</h5>
        <div class="row" id="game-control-table">
          <div class="col-9">
          <table class="game-ctrl-tab">
            <tr>
              <th>主机</th>
              <th>游戏</th>
              <th>状态</th>
              <th>按键接口</th>
              <th>备注</th>
            </tr>
            %for state in game_states:
            <tr>
              <td>{{state[0]}}</td>
              <td>{{state[1]}}</td>
              <td>{{state[2]}}</td>
              <td><button type="button" onclick="pressSpace()">空格</button>
                &nbsp
                <button type="button" onclick="pressEnter()">回车</button>
              </td>
              <td></td>
            </tr>
            %end
          </table>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script src="/static/management_front_end/js/eventhandler.js"></script>
  <script type="text/javascript">
  </script>
</body>
</html>
