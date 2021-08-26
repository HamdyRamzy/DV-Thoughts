
var setTheme = window.localStorage.getItem('theme')
console.log('theme:', setTheme)

if (setTheme == null){
  swapStyle('/static/css/light.css')
}else{
  swapStyle(setTheme)
}

function swapStyle(sheet){
  document.getElementById('mystylesheet').href = sheet
  window.localStorage.setItem('theme', sheet)

}
