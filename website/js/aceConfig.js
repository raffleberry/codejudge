var editor = ace.edit("editor");
editor.setTheme("ace/theme/xcode");
editor.session.setMode("ace/mode/c_cpp");
editor.session.setTabSize(4);
editor.session.setUseSoftTabs(false);
editor.setHighlightActiveLine(false);
document.getElementById('editor').style.fontSize='1em';