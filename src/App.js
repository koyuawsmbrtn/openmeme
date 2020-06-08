import React from 'react';
import './App.css';
import $ from 'jquery';
import config from './config.json';

var translation = {
  "intro": "Use the top right search box to search for a meme and press enter to confirm.",
  "placeholder": "Search for memes...",
  "lookup": "Looking up...",
  "notfound": "Not found."
};

export default class App extends React.Component {
  componentWillMount() {
    var userLang = navigator.language || navigator.userLanguage;
    if (userLang.includes("de")) {
      translation = {
        "intro": "Suche über das obere rechte Eingabefeld, um nach einem Meme zu suchen und drücke Enter um zu bestätigen.",
        "placeholder": "Suche nach Memes...",
        "lookup": "Bitte warten...",
        "notfound": "Nicht gefunden."
      };
    }
  }

  componentDidMount() {
    $("#logo").click(function() {
      window.location.href = "/";
    });

    try {
      function findGetParameter(parameterName) {
        var result = null,
            tmp = [];
        window.location.search
            .substr(1)
            .split("&")
            .forEach(function (item) {
              tmp = item.split("=");
              if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
            });
        return result;
      }

      $("#input_search").val(findGetParameter("q").split("+").join(" "));
      $("#content").html("<div id=\"empty\">"+translation.lookup+"</div>");

      $.get(config.backend+"/"+findGetParameter("q"), function(data) {
        console.log(data);
        $("#content").html("<div style=\"text-align:center\"><a style=\"float:right;padding:10px;\" href=\""+data.split("{{img}}")[1]+"\" target=\"_blank\"><img width=\"150\" src=\""+data.split("{{img}}")[1]+"\"></a><h1>"+data.split(". ")[0]+"</h1><p style=\"text-align:left;\">"+data.split(". ").slice(1).join(". ").split("{{img}}")[0]+"</p></div>");
      }).fail(function() {
        $("#content").html("<div id=\"empty\">"+translation.notfound+"</div>");
      });

    } catch(e) {}
  }
  
  render() {
    return (
      <div className="App">
        <div id="nav">
          <div id="logo">openMeme</div>
          <form>
            <div id="search"><input type="text" placeholder={translation.placeholder} name="q" id="input_search" /></div>
            <input type="submit" style={{display: "none"}} />
          </form>
        </div>
        <div id="content">
        <div id="empty">{translation.intro}</div>
        </div>
      </div>
    );
  }
}