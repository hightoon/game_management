//$("#game-table").append("<h2>mainpage</h2>");

//game table header
gameTabHdr = "<tr><th>HostName</th><th>IP Addr</th><th>Game</th><th>Status</th></tr>";
$("#game-hosts-table").append(gameTabHdr);

gameTab = {
  games: [
    {name: "HostA", ip: "192.168.1.1", game: "basketball", status: "running"},
    {name: "HostB", ip: "192.168.1.2", game: "basketball", status: "running"}
  ]
};

var tdStr = "<td>%data%</td>";

for (gm in gameTab.games) {
  row = "<tr>" +
        tdStr.replace("%data%", gameTab.games[gm].name) +
        tdStr.replace("%data%", gameTab.games[gm].ip) +
        tdStr.replace("%data%", gameTab.games[gm].game) +
        tdStr.replace("%data%", gameTab.games[gm].status) +
        "</tr>";
  $("#game-hosts-table").append(row);
}
